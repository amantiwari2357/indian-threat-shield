package main

import (
	"context"
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/customsiem/agent/internal/collector"
	"github.com/customsiem/agent/internal/config"
	"github.com/customsiem/agent/internal/logger"
	"github.com/customsiem/agent/internal/monitor"
	"github.com/customsiem/agent/internal/processor"
	"github.com/customsiem/agent/internal/sender"
	"github.com/sirupsen/logrus"
	"github.com/spf13/cobra"
)

var (
	version = "1.0.0"
	commit  = "unknown"
	date    = "unknown"
)

func main() {
	rootCmd := &cobra.Command{
		Use:     "custom-siem-agent",
		Short:   "Custom SIEM Agent for log collection and monitoring",
		Version: fmt.Sprintf("%s (commit: %s, date: %s)", version, commit, date),
		RunE:    run,
	}

	// Add flags
	rootCmd.Flags().StringP("config", "c", "", "Path to configuration file")
	rootCmd.Flags().StringP("log-level", "l", "info", "Log level (debug, info, warn, error)")
	rootCmd.Flags().BoolP("daemon", "d", false, "Run as daemon")
	rootCmd.Flags().StringP("agent-id", "i", "", "Agent ID (auto-generated if not provided)")

	if err := rootCmd.Execute(); err != nil {
		os.Exit(1)
	}
}

func run(cmd *cobra.Command, args []string) error {
	// Parse flags
	configPath, _ := cmd.Flags().GetString("config")
	logLevel, _ := cmd.Flags().GetString("log-level")
	daemon, _ := cmd.Flags().GetBool("daemon")
	agentID, _ := cmd.Flags().GetString("agent-id")

	// Initialize logger
	if err := logger.Init(logLevel); err != nil {
		return fmt.Errorf("failed to initialize logger: %w", err)
	}
	log := logger.Get()

	// Load configuration
	cfg, err := config.Load(configPath)
	if err != nil {
		return fmt.Errorf("failed to load configuration: %w", err)
	}

	// Generate agent ID if not provided
	if agentID == "" {
		agentID = generateAgentID()
	}

	log.WithFields(logrus.Fields{
		"agent_id": agentID,
		"version":  version,
		"config":   configPath,
	}).Info("Starting Custom SIEM Agent")

	// Create context with cancellation
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Initialize components
	collector, err := collector.New(cfg.Collector)
	if err != nil {
		return fmt.Errorf("failed to create collector: %w", err)
	}

	processor, err := processor.New(cfg.Processor)
	if err != nil {
		return fmt.Errorf("failed to create processor: %w", err)
	}

	sender, err := sender.New(cfg.Sender, agentID)
	if err != nil {
		return fmt.Errorf("failed to create sender: %w", err)
	}

	monitor, err := monitor.New(cfg.Monitor, agentID)
	if err != nil {
		return fmt.Errorf("failed to create monitor: %w", err)
	}

	// Start components
	if err := collector.Start(ctx); err != nil {
		return fmt.Errorf("failed to start collector: %w", err)
	}
	defer collector.Stop()

	if err := processor.Start(ctx); err != nil {
		return fmt.Errorf("failed to start processor: %w", err)
	}
	defer processor.Stop()

	if err := sender.Start(ctx); err != nil {
		return fmt.Errorf("failed to start sender: %w", err)
	}
	defer sender.Stop()

	if err := monitor.Start(ctx); err != nil {
		return fmt.Errorf("failed to start monitor: %w", err)
	}
	defer monitor.Stop()

	// Connect components
	collector.SetOutput(processor.GetInput())
	processor.SetOutput(sender.GetInput())

	log.Info("Agent started successfully")

	// Handle signals for graceful shutdown
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Wait for shutdown signal
	select {
	case sig := <-sigChan:
		log.WithField("signal", sig).Info("Received shutdown signal")
	case <-ctx.Done():
		log.Info("Context cancelled")
	}

	// Graceful shutdown
	log.Info("Shutting down agent...")
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer shutdownCancel()

	// Stop components in reverse order
	monitor.Stop()
	sender.Stop()
	processor.Stop()
	collector.Stop()

	log.Info("Agent shutdown complete")
	return nil
}

func generateAgentID() string {
	bytes := make([]byte, 16)
	if _, err := rand.Read(bytes); err != nil {
		// Fallback to timestamp-based ID
		return fmt.Sprintf("agent-%d", time.Now().Unix())
	}
	return hex.EncodeToString(bytes)
} 