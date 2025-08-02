package com.customsiem.controller;

import com.customsiem.model.Agent;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.time.LocalDateTime;
import java.util.*;

/**
 * Agent management controller for Custom SIEM
 */
@RestController
@RequestMapping("/agents")
@CrossOrigin(origins = "*")
public class AgentController {

    // Temporary in-memory storage for demo
    private final Map<String, Agent> agents = new HashMap<>();

    @GetMapping
    public ResponseEntity<List<Agent>> getAllAgents() {
        return ResponseEntity.ok(new ArrayList<>(agents.values()));
    }

    @GetMapping("/{agentId}")
    public ResponseEntity<Agent> getAgent(@PathVariable String agentId) {
        Agent agent = agents.get(agentId);
        if (agent == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(agent);
    }

    @PostMapping("/register")
    public ResponseEntity<Agent> registerAgent(@RequestBody Agent agent) {
        agent.setAgentId(UUID.randomUUID().toString());
        agent.setRegistrationDate(LocalDateTime.now());
        agent.setStatus(Agent.AgentStatus.ACTIVE);
        agent.setLastHeartbeat(LocalDateTime.now());
        
        agents.put(agent.getAgentId(), agent);
        
        return ResponseEntity.ok(agent);
    }

    @PostMapping("/{agentId}/heartbeat")
    public ResponseEntity<Map<String, Object>> heartbeat(@PathVariable String agentId) {
        Agent agent = agents.get(agentId);
        if (agent == null) {
            return ResponseEntity.notFound().build();
        }
        
        agent.setLastHeartbeat(LocalDateTime.now());
        agent.setStatus(Agent.AgentStatus.ACTIVE);
        
        Map<String, Object> response = new HashMap<>();
        response.put("status", "OK");
        response.put("timestamp", LocalDateTime.now());
        response.put("agentId", agentId);
        
        return ResponseEntity.ok(response);
    }

    @DeleteMapping("/{agentId}")
    public ResponseEntity<Void> deleteAgent(@PathVariable String agentId) {
        Agent agent = agents.remove(agentId);
        if (agent == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok().build();
    }
} 