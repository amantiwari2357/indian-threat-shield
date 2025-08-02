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
 * Entity representing an agent group
 */
@Entity
@Table(name = "agent_groups")
@EntityListeners(AuditingEntityListener.class)
public class AgentGroup {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank
    @Column(name = "group_id", unique = true, nullable = false)
    private String groupId;

    @NotBlank
    @Column(nullable = false)
    private String name;

    @Column(length = 1000)
    private String description;

    @Column(name = "created_at", nullable = false, updatable = false)
    @CreatedDate
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    @LastModifiedDate
    private LocalDateTime updatedAt;

    @Column(name = "created_by")
    private String createdBy;

    @Column(name = "is_system_group")
    private boolean systemGroup = false;

    @Column(name = "is_active")
    private boolean active = true;

    @OneToMany(mappedBy = "group", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private Set<Agent> agents = new HashSet<>();

    // Constructors
    public AgentGroup() {}

    public AgentGroup(String groupId, String name) {
        this.groupId = groupId;
        this.name = name;
    }

    // Getters and Setters
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getGroupId() {
        return groupId;
    }

    public void setGroupId(String groupId) {
        this.groupId = groupId;
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

    public boolean isSystemGroup() {
        return systemGroup;
    }

    public void setSystemGroup(boolean systemGroup) {
        this.systemGroup = systemGroup;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    public Set<Agent> getAgents() {
        return agents;
    }

    public void setAgents(Set<Agent> agents) {
        this.agents = agents;
    }

    // Helper methods
    public void addAgent(Agent agent) {
        this.agents.add(agent);
        agent.setGroup(this);
    }

    public void removeAgent(Agent agent) {
        this.agents.remove(agent);
        agent.setGroup(null);
    }

    public int getAgentCount() {
        return agents.size();
    }

    public int getActiveAgentCount() {
        return (int) agents.stream()
                .filter(Agent::isActive)
                .count();
    }

    public int getOnlineAgentCount() {
        return (int) agents.stream()
                .filter(Agent::isOnline)
                .count();
    }

    @Override
    public String toString() {
        return "AgentGroup{" +
                "id=" + id +
                ", groupId='" + groupId + '\'' +
                ", name='" + name + '\'' +
                ", active=" + active +
                ", agentCount=" + getAgentCount() +
                '}';
    }
} 