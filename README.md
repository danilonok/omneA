# 🤖 OmneA - Intelligent Windows Assistant 

**OmneA** is a diploma project built on a **multi-agent architecture** powered by Large Language Models (LLMs). It functions as an intelligent assistant designed to provide comprehensive control and automation for the Windows Operating System.

## Features 

* **Comprehensive OS Control:** OmneA controls your PC's functionalities, simulating the actions of a real user. 
* **ReAct-Style Multi-Agent Orchestration:** Utilizes a ReAct (Reasoning and Acting) framework for advanced task handling and agent communication. 
* **Modular Agent System:** Built with 6 distinct functional agents capable of fulfilling diverse user tasks. The modular design allows for easy integration of new agents. 
* **High Security:** Features strict permission control and task filters to ensure secure and regulated system interactions.
* **Modern and Minimalistic UI:** Provides a convenient user experience through a modern graphical interface. 
* **Thorough Inspection:** Includes a detailed log-system for complete inspection and control of agent activities.

## System Architecture

OmneA employs a modular Client-Server architecture, ensuring a clear separation between the GUI (Client) and the business logic (Server). 

### Key Components 

* **Agent-Orchestrator (ReAct Agent):** Manages and controls the entire multi-agent infrastructure.
* **Functional Agents (4 Agents):** Control core Windows functions (e.g., FileAgent, MediaControlAgent, WebSearchAgent).
* **PowershellAgent (ReAct Agent):** Enables full OS control via CMD/Powershell for complex scenarios. 
* **Agentic Infrastructure (Server):** Built with LlamaIndex and FastAPI, providing consistent **Websocket** connections. 
* **GUI Layer (ElectronJS App):** The client application, offering the modern user interface.

## Technologies Used 

* OmneA leverages several powerful frameworks to create its multi-agent system:
* **LlamaIndex:** Core framework for the agentic infrastructure and tool orchestration.
* **FastAPI:** High-performance Python framework for the server-side API and Websocket management.
* **ElectronJS:** Used to build the cross-platform, modern graphical user interface (GUI) client.

## 🎓 Diploma Project Status 

This repository hosts the source code for the OmneA intelligent assistant, developed as a diploma project.
