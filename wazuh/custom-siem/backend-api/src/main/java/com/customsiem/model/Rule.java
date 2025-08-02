package com.customsiem.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.annotation.LastModifiedDate;
import org.springframework.data.jpa.domain.support.AuditingEntityListener;

import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

/**
 * Entity representing a detection rule
 */
@Entity
@Table(name = "rules")
@EntityListeners(AuditingEntityListener.class)
public class Rule {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(name = "rule_id", unique = true, nullable = false)
    private String ruleId;

    @NotBlank
    @Column(nullable = false)
    private String name;

    @Column(length = 2000)
    private String description;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RuleType type = RuleType.CORRELATION;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private RuleStatus status = RuleStatus.ACTIVE;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Alert.AlertLevel alertLevel = Alert.AlertLevel.MEDIUM;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Alert.AlertCategory alertCategory = Alert.AlertCategory.SECURITY;

    @Column(name = "pattern", columnDefinition = "TEXT", nullable = false)
    private String pattern;

    @Column(name = "condition", columnDefinition = "TEXT")
    private String condition;

    @Column(name = "frequency")
    private Integer frequency; // Number of events within time window

    @Column(name = "time_window")
    private Integer timeWindow; // Time window in seconds

    @Column(name = "threshold")
    private Integer threshold;

    @Column(name = "mitre_attack_technique")
    private String mitreAttackTechnique;

    @Column(name = "compliance_framework")
    private String complianceFramework;

    @Column(name = "tags")
    private String tags; // Comma-separated tags

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreatedDate
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Column(name = "created_by")
    private String createdBy;

    @Column(name = "is_system_rule")
    private boolean systemRule = false;

    @Column(name = "is_enabled")
    private boolean enabled = true;

    @OneToMany(mappedBy = "rule", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Set<Alert> alerts = new HashSet<>();

    // Constructors
    public Rule() {}

    public Rule(String ruleId, String name, String pattern) {
        this.ruleId = ruleId;
        this.name = name;
        this.pattern = pattern;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getRuleId() {
        return ruleId;
    }

    public void setRuleId(String ruleId) {
        this.ruleId = ruleId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public RuleType getType() {
        return type;
    }

    public void setType(RuleType type) {
        this.type = type;
    }

    public RuleStatus getStatus() {
        return status;
    }

    public void setStatus(RuleStatus status) {
        this.status = status;
    }

    public Alert.AlertLevel getAlertLevel() {
        return alertLevel;
    }

    public void setAlertLevel(Alert.AlertLevel alertLevel) {
        this.alertLevel = alertLevel;
    }

    public Alert.AlertCategory getAlertCategory() {
        return alertCategory;
    }

    public void setAlertCategory(Alert.AlertCategory alertCategory) {
        this.alertCategory = alertCategory;
    }

    public String getPattern() {
        return pattern;
    }

    public void setPattern(String pattern) {
        this.pattern = pattern;
    }

    public String getCondition() {
        return condition;
    }

    public void setCondition(String condition) {
        this.condition = condition;
    }

    public Integer getFrequency() {
        return frequency;
    }

    public void setFrequency(Integer frequency) {
        this.frequency = frequency;
    }

    public Integer getTimeWindow() {
        return timeWindow;
    }

    public void setTimeWindow(Integer timeWindow) {
        this.timeWindow = timeWindow;
    }

    public Integer getThreshold() {
        return threshold;
    }

    public void setThreshold(Integer threshold) {
        this.threshold = threshold;
    }

    public String getMitreAttackTechnique() {
        return mitreAttackTechnique;
    }

    public void setMitreAttackTechnique(String mitreAttackTechnique) {
        this.mitreAttackTechnique = mitreAttackTechnique;
    }

    public String getComplianceFramework() {
        return complianceFramework;
    }

    public void setComplianceFramework(String complianceFramework) {
        this.complianceFramework = complianceFramework;
    }

    public String getTags() {
        return tags;
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public LocalDateTime getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(LocalDateTime updatedAt) {
        this.updatedAt = updatedAt;
    }

    public String getCreatedBy() {
        return createdBy;
    }

    public void setCreatedBy(String createdBy) {
        this.createdBy = createdBy;
    }

    public boolean isSystemRule() {
        return systemRule;
    }

    public void setSystemRule(boolean systemRule) {
        this.systemRule = systemRule;
    }

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public Set<Alert> getAlerts() {
        return alerts;
    }

    public void setAlerts(Set<Alert> alerts) {
        this.alerts = alerts;
    }

    // Helper methods
    public boolean isActive() {
        return status == RuleStatus.ACTIVE && enabled;
    }

    public void enable() {
        this.enabled = true;
        this.status = RuleStatus.ACTIVE;
    }

    public void disable() {
        this.enabled = false;
        this.status = RuleStatus.INACTIVE;
    }

    public boolean isCorrelationRule() {
        return type == RuleType.CORRELATION;
    }

    public boolean isThresholdRule() {
        return type == RuleType.THRESHOLD;
    }

    public boolean isPatternRule() {
        return type == RuleType.PATTERN;
    }

    @Override
    public String toString() {
        return "Rule{" +
                "id=" + id +
                ", ruleId='" + ruleId + '\'' +
                ", name='" + name + '\'' +
                ", type=" + type +
                ", status=" + status +
                ", enabled=" + enabled +
                '}';
    }

    /**
     * Enum for rule types
     */
    public enum RuleType {
        PATTERN,        // Simple pattern matching
        CORRELATION,    // Event correlation
        THRESHOLD,      // Threshold-based
        ANOMALY,        // Anomaly detection
        COMPLIANCE      // Compliance rules
    }

    /**
     * Enum for rule status
     */
    public enum RuleStatus {
        ACTIVE,
        INACTIVE,
        DRAFT,
        TESTING
    }
} 