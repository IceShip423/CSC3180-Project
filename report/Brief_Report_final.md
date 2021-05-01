# Brief Report

## Project Information

Topic: AI-driven Drone swarm —The application in reconnaissance and attack

Group member:

| Name   | Student ID |
| ------ | ---------- |
| 禹思南 | 117010365  |
| 李鼎   | 119010144  |
| 吴伊凡 | 118020064  |
| 陈秋泓 | 119010025  |

## Background

Unmanned aerial vehicle(UAV) is a powerful platform that has the ability to autonomously cruise and complete assigned tasks. People only give commands to UAVs and do not control the way that they work in. All tasks are completed all by UAV.  Recently UAVs have been applied to many industries like transportation and the military. In transportation, UAV can decrease the cost significantly. In the military, UAVs are cheap compared to missiles and have a large threat to the enemy. Therefore to complete different kinds of tasks, UAVs need lots of different systems. The basic systems of UAV contain Multi-UAV supervision and control system, attitude control system, obstacle avoidance system, route planning system, and so on. 

## Project Architecture

### Implementation Goal

An AI-driven Drone swarm that can cruise while avoiding obstacles respectively, and furthermore, accomplish reconnaissance missions or attack missions with optimal route. 

The information of the environment (a map including obstacles) and the positions of targets are transmitted to the program. The agent should be able to lead the drone swarm to target places and complete reconnaissance missions or attack missions.

### Component

1. Cruise and obstacle avoidance
2. Reconnaissance AI agent
3. Attack AI agent
4. GUI that can reflect the motions of drome swarm over time

### Key Design

We make the environment static and deterministic to simplify the problem. The environment remains partially observable to the agents. 

In this project, we simplify the process of searching for information. In practice, UAVs take photos through cameras and distract information from photos, and then find targets through the algorithm. Here we use a radius r to denote the search field  of a UAV and assume UAV will always find the objects immediately when the distance between objects and UAV is less than r. We also simplify the altitude control system and use velocity vector in 2D coordinate to denote the basic movement of UAV.

We design an algorithm to control the basic actions of drones warm so that they can complete the tasks together. The obstacle system and route planning system will return positions in [x,y] form to automatically tell the drone swarm where to move and avoid collisions.

### Platform

The implementation is based on Python. Additionally, the outcome should be visible from a graphical interface based on the turtle package.

 

 