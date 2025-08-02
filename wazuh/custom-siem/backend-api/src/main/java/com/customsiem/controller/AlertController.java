package com.customsiem.controller;

import com.customsiem.model.Alert;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.time.LocalDateTime;
import java.util.*;

/**
 * Alert management controller for Custom SIEM
 */
@RestController
@RequestMapping("/alerts")
@CrossOrigin(origins = "*")
public class AlertController {

    // Temporary in-memory storage for demo
    private final Map<String, Alert> alerts = new HashMap<>();

    @GetMapping
    public ResponseEntity<List<Alert>> getAllAlerts(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "50") int size,
            @RequestParam(required = false) String level,
            @RequestParam(required = false) String status) {
        
        List<Alert> allAlerts = new ArrayList<>(alerts.values());
        
        // Simple filtering
        if (level != null) {
            allAlerts = allAlerts.stream()
                .filter(alert -> level.equals(alert.getLevel().toString()))
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
        }
        
        if (status != null) {
            allAlerts = allAlerts.stream()
                .filter(alert -> status.equals(alert.getStatus().toString()))
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
        }
        
        // Simple pagination
        int start = page * size;
        int end = Math.min(start + size, allAlerts.size());
        
        if (start >= allAlerts.size()) {
            return ResponseEntity.ok(new ArrayList<>());
        }
        
        return ResponseEntity.ok(allAlerts.subList(start, end));
    }

    @GetMapping("/{alertId}")
    public ResponseEntity<Alert> getAlert(@PathVariable String alertId) {
        Alert alert = alerts.get(alertId);
        if (alert == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(alert);
    }

    @PostMapping
    public ResponseEntity<Alert> createAlert(@RequestBody Alert alert) {
        alert.setAlertId(UUID.randomUUID().toString());
        alert.setCreatedAt(LocalDateTime.now());
        alert.setUpdatedAt(LocalDateTime.now());
        
        if (alert.getStatus() == null) {
            alert.setStatus(Alert.AlertStatus.OPEN);
        }
        
        alerts.put(alert.getAlertId(), alert);
        
        return ResponseEntity.ok(alert);
    }

    @PutMapping("/{alertId}")
    public ResponseEntity<Alert> updateAlert(@PathVariable String alertId, @RequestBody Alert alert) {
        Alert existingAlert = alerts.get(alertId);
        if (existingAlert == null) {
            return ResponseEntity.notFound().build();
        }
        
        alert.setAlertId(alertId);
        alert.setUpdatedAt(LocalDateTime.now());
        alert.setCreatedAt(existingAlert.getCreatedAt());
        
        alerts.put(alertId, alert);
        
        return ResponseEntity.ok(alert);
    }

    @DeleteMapping("/{alertId}")
    public ResponseEntity<Void> deleteAlert(@PathVariable String alertId) {
        Alert alert = alerts.remove(alertId);
        if (alert == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok().build();
    }

    @GetMapping("/stats")
    public ResponseEntity<Map<String, Object>> getAlertStats() {
        Map<String, Object> stats = new HashMap<>();
        
        long totalAlerts = alerts.size();
        long openAlerts = alerts.values().stream()
            .filter(alert -> alert.getStatus() == Alert.AlertStatus.OPEN)
            .count();
        long criticalAlerts = alerts.values().stream()
            .filter(alert -> alert.getLevel() == Alert.AlertLevel.CRITICAL)
            .count();
        
        stats.put("totalAlerts", totalAlerts);
        stats.put("openAlerts", openAlerts);
        stats.put("criticalAlerts", criticalAlerts);
        stats.put("timestamp", LocalDateTime.now());
        
        return ResponseEntity.ok(stats);
    }
} 