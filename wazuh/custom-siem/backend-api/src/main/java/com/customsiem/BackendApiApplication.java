package com.customsiem;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.data.jpa.repository.config.EnableJpaAuditing;

/**
 * Main application class for Custom SIEM Backend API
 * 
 * This application provides:
 * - RESTful APIs for dashboard and agent communication
 * - Authentication and authorization
 * - Log processing and alert generation
 * - Integration with Elasticsearch and Kafka
 * - User management and role-based access control
 */
@SpringBootApplication
@EnableScheduling
@EnableJpaAuditing
public class BackendApiApplication {

    public static void main(String[] args) {
        SpringApplication.run(BackendApiApplication.class, args);
    }
} 