# OpenBlueprint — Design Model

## 1. Purpose

The Design Model is the canonical structured representation of an OpenBlueprint project.

It is the source of truth from which the user interface, diagrams, validation engines, simulation adapters, BOM generation, documentation, and exports are derived.

The AI must not be treated as the source of truth.

---

## 2. Design Hierarchy

An OpenBlueprint design follows a hierarchical structure:

Design
├── Requirements
├── Systems
│   ├── Subsystems
│   │   ├── Components
│   │   └── Resources
│   └── Interfaces
├── Connections
├── Constraints
├── Parameters
├── Validation Rules
├── Simulation Configuration
├── Validation Results
├── Design Decisions
├── BOM
└── Documentation

The hierarchy must support arbitrary depth where necessary.

---

## 3. Design

A Design represents the complete technical project.

A Design should contain at minimum:

- Unique identifier
- Name
- Description
- Version
- Requirements
- Systems
- Connections
- Constraints
- Parameters
- Validation state
- Simulation state
- BOM
- Metadata

A Design must be serializable into a human-readable and machine-readable format.

---

## 4. Requirements

A Requirement represents something the final design must satisfy.

Examples:

- Operating voltage must be 12 V
- System must operate for at least 8 hours
- Device must weigh less than 2 kg
- Communication range must exceed 1 km
- Temperature must remain between -20 °C and 60 °C
- Response time must remain below 100 ms

Requirements may be:

- Functional
- Electrical
- Mechanical
- Thermal
- Software
- Performance
- Environmental
- Safety
- Cost
- Regulatory
- User-defined

Requirements should support measurable constraints where possible.

---

## 5. Systems

A System represents a functional or physical grouping of elements.

Examples:

- Power system
- Control system
- Communication system
- Sensing system
- Propulsion system
- User interface
- Data-processing system

Systems may contain other systems.

This allows hierarchical decomposition.

Example:

System
└── UAV
    ├── Flight Control
    ├── Power
    ├── Communication
    └── Payload

The same mechanism must work for non-UAV projects.

---

## 6. Components

A Component represents a concrete element used by a design.

Examples:

- Microcontroller
- Sensor
- Motor
- Battery
- Resistor
- Gear
- Structural element
- Software library
- Processor
- Communication module

A Component may have:

- Identifier
- Name
- Manufacturer
- Part number
- Type
- Specifications
- Interfaces
- Operating limits
- Physical properties
- Cost information
- Datasheet references
- Simulation model
- Metadata

Components should be reusable across projects.

---

## 7. Resources

A Resource represents something required by a system but not necessarily a physical component.

Examples:

- CPU time
- Memory
- GPIO pins
- Network bandwidth
- Electrical power
- Storage
- Manufacturing capacity
- Budget
- Weight allowance

Resources can have limits and consumption values.

---

## 8. Interfaces

An Interface describes how one element communicates, connects, or interacts with another.

Examples:

- GPIO
- UART
- SPI
- I2C
- CAN
- Ethernet
- USB
- Analog signal
- PWM
- Mechanical interface
- Electrical power interface
- Software API

An interface should define compatibility requirements where known.

---

## 9. Connections

A Connection represents a relationship between two or more elements.

A connection may describe:

- Source
- Destination
- Interface
- Signal
- Direction
- Data type
- Voltage
- Current
- Frequency
- Protocol
- Physical characteristics
- Constraints

Connections must be independently represented from visual diagram edges.

The diagram is only a visualization of connections.

---

## 10. Constraints

A Constraint represents a condition that the design must satisfy.

Examples:

- Maximum voltage
- Minimum battery capacity
- Maximum weight
- Maximum temperature
- Maximum current
- Required interface
- Minimum communication range
- Maximum cost

Constraints may apply to:

- Entire design
- System
- Subsystem
- Component
- Connection
- Requirement

---

## 11. Parameters

Parameters represent values that may change during design or simulation.

Examples:

- Voltage
- Current
- Resistance
- Capacitance
- Mass
- Dimensions
- Temperature
- Speed
- Frequency
- Battery capacity
- PID gains

Parameters should support units where applicable.

---

## 12. Validation

Validation operates on the Design Model.

Validation rules should be able to inspect:

- Requirements
- Components
- Interfaces
- Connections
- Constraints
- Parameters
- Resources

Validation results should contain:

- Rule identifier
- Severity
- Status
- Message
- Affected objects
- Evidence
- Suggested correction where available

Severity levels:

- INFO
- WARNING
- ERROR
- UNKNOWN

---

## 13. Simulation

Simulation configuration references an appropriate simulation engine.

The Design Model should contain enough structured information for an adapter to translate the design into the target simulator's format.

Simulation results should be stored separately from the design itself.

Results may contain:

- Simulation identifier
- Simulator
- Version
- Configuration
- Input parameters
- Output measurements
- Logs
- Errors
- Generated artifacts
- Result status

---

## 14. Design Decisions

A Design Decision records important decisions made during development.

Examples:

- Why a particular component was selected
- Why an alternative was rejected
- Why a particular architecture was chosen
- What assumption was made
- What trade-off was accepted

AI-generated decisions should be distinguishable from user-approved decisions.

---

## 15. Bill of Materials

The BOM is generated from the Design Model.

A BOM item may contain:

- Component identifier
- Part number
- Description
- Manufacturer
- Quantity
- Unit cost
- Total cost
- Supplier
- Lifecycle status
- Alternatives

The BOM should never be maintained independently from the underlying design.

---

## 16. Versioning

Every saved design should be versionable.

Changes should eventually be traceable to:

- User modification
- AI modification
- Imported data
- Validation correction
- Simulation result
- External tool

The system should eventually support comparison between design versions.

---

## 17. Domain Independence

The Design Model must not contain assumptions that make it specific to a particular engineering domain.

Domain-specific information should be represented through:

- Component types
- Interfaces
- Constraints
- Parameters
- Validation rules
- Simulation adapters
- Plugins
- Knowledge modules

The core Design Model remains domain-independent.

---

## 18. Canonical Representation

The Design Model is authoritative.

Other representations are derived from it:

Design Model
├── UI
├── Diagram
├── BOM
├── Validation
├── Simulation
├── Documentation
├── KiCad export
├── CAD export
└── Other integrations

No derived representation should silently modify the underlying design without creating an explicit design change.

---

## 19. AI Boundary

The AI may propose changes to the Design Model.

The application must validate and apply those changes through controlled operations.

The AI should not have unrestricted direct access to the underlying project state.

Conceptually:

User
→ AI
→ Proposed Changes
→ Schema Validation
→ Engineering Validation
→ User Approval where required
→ Design Model

This separation is a core safety and reliability requirement.