# Code-to-Documentation Linking Guidelines

This document provides comprehensive guidelines for linking code to documentation in the Bee Organized PWA, ensuring that developers can easily understand the business context, architectural decisions, and implementation patterns behind any piece of code.

## Overview

Code-to-documentation linking is a critical practice that:
- **Preserves Context**: Maintains connection between code and business requirements
- **Supports Maintenance**: Helps future developers understand why code exists and how it should be modified
- **Enables Onboarding**: Allows new team members to quickly understand system design and constraints
- **Facilitates Review**: Provides reviewers with context for evaluating code changes

## Linking Responsibilities

### **TDD Software Engineer Agent - PRIMARY RESPONSIBILITY**
- **MUST add documentation links** to all new code implementations
- **MUST follow linking standards** for consistency and discoverability
- **MUST validate link accuracy** before marking implementation complete
- **SHOULD update links** when documentation structure changes

### **Software Architect Agent**
- **SHOULD validate** that architectural implementations reference appropriate design decisions
- **SHOULD ensure** that architectural patterns are properly documented and linked
- **SHOULD coordinate** documentation updates that affect multiple code references

### **QA Test Validator Agent**
- **MUST verify** that code includes appropriate documentation references
- **MUST validate** that documentation links are accurate and current
- **SHOULD check** that implementation follows documented patterns and requirements

## Documentation Reference Structure

### **Documentation Hierarchy**
```
/docs/
├── requirements/{file}.md#{section}    # Business requirements and user stories
├── architecture/{file}.md#{section}    # Technical architecture and design
├── patterns/{file}.md#{section}        # Development patterns and conventions
├── decisions/{file}.md                 # Architecture Decision Records (ADRs)
└── guides/{file}.md#{section}          # Process and operational guides
```

### **Link Format Standards**
All documentation references should use this format:
- **Full Path**: `/docs/{category}/{filename}.md#{section-anchor}`
- **Relative References**: When linking from within docs, use relative paths: `../category/filename.md#{section}`
- **Section Anchors**: Always include specific section when referencing particular content

## Code Commenting Patterns

### **Class and Component Documentation**

#### **React Components**
```javascript
/**
 * Hive inspection form component for field data collection
 * Requirements: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Hive-level inspection
 * Architecture: /docs/architecture/component-patterns.md#inspection-forms
 * Patterns: /docs/patterns/code-conventions.md#form-validation
 */
class HiveInspectionForm extends React.Component {
  /**
   * Validates temperament assessment input (1-5 scale)
   * Requirements: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Temperament assessment
   * Patterns: /docs/patterns/error-handling.md#user-input-validation
   */
  validateTemperament(rating) {
    // Implementation follows documented 1-5 scale requirements
    // 1-2: Bell pepper (calm), 3: Neutral, 4-5: Chili pepper (aggressive)
    if (rating < 1 || rating > 5) {
      throw new ValidationError('Temperament rating must be between 1 and 5');
    }
    return rating;
  }
}
```

#### **Service Classes**
```javascript
/**
 * Data service for managing inspection records and sync operations
 * Architecture: /docs/architecture/data-models.md#inspection-entities
 * Architecture: /docs/architecture/integration-points.md#indexeddb-sync
 * Patterns: /docs/patterns/performance-guidelines.md#database-operations
 */
class InspectionDataService {
  /**
   * Resolves entity identifiers for history display
   * Architecture: /docs/architecture/data-models.md#id-resolution-pattern
   * Requirements: /docs/requirements/inspection-history-system.md#identifier-display
   */
  async resolveEntityIdentifier(entityType, id) {
    // Implementation follows documented ID resolution pattern
    // See: /docs/DESIGN.md#id-resolution-pattern for complete approach
  }
}
```

### **Business Logic Documentation**

#### **Complex Business Rules**
```javascript
/**
 * Calculates box inspection summary from frame data
 * Requirements: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Box-level inspection
 * Architecture: /docs/architecture/data-models.md#inspection-rollups
 */
const calculateBoxSummary = (frameInspections) => {
  // Box inspection is rollup of frame inspections within the box
  // Requirements specify validation: percentages should total (frames × 100)
  // See: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Summary display requirements

  const totalPercentages = frameInspections.reduce((sum, frame) => {
    // Percentage calculation follows documented validation rules
    // See: /docs/patterns/code-conventions.md#percentage-calculations
    return sum + (frame.nectar + frame.honey + frame.brood + frame.empty);
  }, 0);

  const expectedTotal = frameInspections.length * 100;
  if (Math.abs(totalPercentages - expectedTotal) > 5) {
    // Error handling follows documented patterns
    // See: /docs/patterns/error-handling.md#validation-errors
    console.warn(`Box summary validation: expected ${expectedTotal}, got ${totalPercentages}`);
  }

  return {
    totalNectar: frameInspections.reduce((sum, f) => sum + f.nectar, 0),
    totalHoney: frameInspections.reduce((sum, f) => sum + f.honey, 0),
    totalBrood: frameInspections.reduce((sum, f) => sum + f.brood, 0),
    totalEmpty: frameInspections.reduce((sum, f) => sum + f.empty, 0),
    frameCount: frameInspections.length,
    validationPassed: Math.abs(totalPercentages - expectedTotal) <= 5
  };
};
```

#### **Algorithm Implementation**
```javascript
/**
 * Conflict resolution algorithm for offline sync operations
 * Architecture: /docs/architecture/integration-points.md#conflict-resolution
 * Decisions: /docs/decisions/002-offline-storage.md
 */
const resolveDataConflict = (localData, remoteData) => {
  // Conflict resolution follows documented timestamp-based approach
  // See: /docs/DESIGN.md#conflict-detection-logic

  if (!localData.lastModified || !remoteData.lastModified) {
    // Handle missing timestamps per architectural decision
    // See: /docs/decisions/002-offline-storage.md#timestamp-handling
    return remoteData; // Default to remote when timestamps unavailable
  }

  const localTime = new Date(localData.lastModified);
  const remoteTime = new Date(remoteData.lastModified);

  // Most recent timestamp wins per documented algorithm
  return localTime > remoteTime ? localData : remoteData;
};
```

### **Configuration and Setup Documentation**

#### **Database Schema Implementation**
```javascript
/**
 * IndexedDB schema definition for beekeeping data model
 * Architecture: /docs/architecture/data-models.md#database-schema
 * Architecture: /docs/DESIGN.md#storage-mapping
 */
const schema = {
  // Table definitions follow documented data model
  // See: /docs/architecture/data-models.md#core-entities
  hives: "++id, identifier, location, notes",
  boxes: "++id, serialNumber, size, currentHiveId",
  frames: "++id, serialNumber, currentBoxId",

  // History tables per architectural decision for assignment tracking
  // See: /docs/DESIGN.md#assignment-history-storage
  boxHistory: "++id, boxId, dateAdded, dateRemoved, position, hiveId, notes",
  frameHistory: "++id, frameId, dateAdded, dateRemoved, position, boxId, notes",

  // Inspection data model separation per requirements
  // See: GitHub Issue I-3 (https://github.com/badvision/bee-organized/issues/4) - Inspection data model separation
  inspectionSessions: "++id, hiveId, sessionDate, temperament, *problems",
  frameInspections: "++id, frameId, sessionId, nectar, honey, brood, empty, *observations"
};
```

#### **API Integration**
```javascript
/**
 * Google Sheets API integration for cloud synchronization
 * Architecture: /docs/architecture/integration-points.md#google-sheets-sync
 * Decisions: /docs/decisions/001-pwa-architecture.md
 */
class GoogleSheetsService {
  /**
   * Batch upload operations for efficient API usage
   * Architecture: /docs/DESIGN.md#sync-considerations
   * Patterns: /docs/patterns/performance-guidelines.md#api-optimization
   */
  async batchUpload(entities, sheetName) {
    // Batch operations to minimize API calls per documented approach
    // See: /docs/DESIGN.md#sync-considerations

    const batchSize = 100; // Per performance guidelines
    const batches = this.createBatches(entities, batchSize);

    // Error handling follows documented retry patterns
    // See: /docs/patterns/error-handling.md#api-retry-logic
    for (const batch of batches) {
      try {
        await this.uploadBatch(batch, sheetName);
      } catch (error) {
        // Retry logic per documented patterns
        await this.handleUploadError(error, batch, sheetName);
      }
    }
  }
}
```

### **Utility and Helper Function Documentation**

#### **Validation Utilities**
```javascript
/**
 * Form validation utilities for beekeeping data input
 * Patterns: /docs/patterns/code-conventions.md#validation-patterns
 * Requirements: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Validation requirements
 */
const ValidationUtils = {
  /**
   * Validates serial number format for equipment tracking
   * Requirements: /docs/requirements/hive-component.md#serial-number-format
   * Patterns: /docs/patterns/error-handling.md#input-validation
   */
  validateSerialNumber(serialNumber) {
    // Serial number validation per documented requirements
    // Format requirements defined in hive component specification
    const pattern = /^[A-Z]{2,3}-\d{3,6}$/;
    return pattern.test(serialNumber);
  },

  /**
   * Validates percentage values for inspection data entry
   * Requirements: GitHub Issue I-4 (https://github.com/badvision/bee-organized/issues/5) - Frame-level inspection
   */
  validatePercentage(value) {
    // Percentage validation follows documented business rules
    // Must be 0-100, allows decimals for precision
    return typeof value === 'number' && value >= 0 && value <= 100;
  }
};
```

#### **Data Transformation Utilities**
```javascript
/**
 * Data transformation utilities for Google Sheets sync operations
 * Architecture: /docs/DESIGN.md#data-transformation
 * Architecture: /docs/architecture/integration-points.md#sheets-mapping
 */
const DataTransformUtils = {
  /**
   * Transforms assignment history for Google Sheets export
   * Architecture: /docs/DESIGN.md#assignment-history-storage
   */
  transformHistoryForExport(historyRecords) {
    // Transform per documented Google Sheets mapping
    // See: /docs/DESIGN.md#google-sheets-mapping for column structure
    return historyRecords.map(record => [
      record.id,
      record.entityId,
      record.dateAdded,
      record.dateRemoved || '', // Empty string for ongoing assignments
      record.position || '',
      record.parentId || '',
      record.notes || ''
    ]);
  }
};
```

## Link Maintenance Guidelines

### **When to Update Links**
1. **Documentation Restructuring**: When docs are moved or renamed, update all code references
2. **Section Changes**: When documentation sections are renamed or restructured
3. **New Documentation**: When new docs are created that are more specific than existing references
4. **Deprecated Documentation**: When old docs are replaced or removed

### **Link Validation Process**
1. **Development Time**: Validate links work when writing code
2. **Code Review**: Reviewers check that links are accurate and helpful
3. **Documentation Updates**: When docs change, search codebase for affected references
4. **Periodic Audits**: Regular validation of link accuracy across codebase

### **Link Update Tools and Techniques**

#### **Finding References**
```bash
# Find all documentation references in code
rg "/docs/" --type js --type jsx -n

# Find references to specific documentation files
rg "GitHub Issue I-4" --type js -n

# Find references to specific sections
rg "#temperament-assessment" --type js -n
```

#### **Batch Reference Updates**
```bash
# Update file references after documentation moves
find src/ -name "*.js" -o -name "*.jsx" | xargs sed -i 's|/docs/old/path|/docs/new/path|g'

# Update section references after restructuring
find src/ -name "*.js" -o -name "*.jsx" | xargs sed -i 's|#old-section|#new-section|g'
```

## Quality Standards

### **Reference Quality Criteria**
- **Accurate**: Links point to correct, current documentation locations
- **Specific**: References include section anchors for precise context
- **Helpful**: Links provide relevant context for understanding the code
- **Current**: References remain valid as documentation evolves
- **Complete**: All major business logic and architectural decisions are referenced

### **Coverage Guidelines**

#### **Required References**
- **Public APIs**: All public classes, methods, and components
- **Business Logic**: Complex algorithms and business rule implementations
- **Configuration**: Database schemas, API integrations, and system setup
- **Validation**: Input validation and error handling logic

#### **Optional References**
- **Utility Functions**: Simple, self-explanatory helper functions
- **Standard Patterns**: Well-established patterns that don't require explanation
- **Temporary Code**: Short-term implementations or debugging code

## Integration with Development Workflow

### **Agent Responsibilities**

#### **During Development**
- **TDD Software Engineer**: Add appropriate documentation references to all new code
- **Code Reviewers**: Validate that references are accurate and helpful
- **QA Validator**: Verify documentation links as part of quality validation

#### **During Documentation Updates**
- **Technical Analyst**: Update requirement references when requirements change
- **Software Architect**: Update architecture and decision references when designs change
- **Documentation Maintainers**: Search for and update code references when docs change

### **Quality Gates**
- **Code Completion**: All new code includes appropriate documentation references
- **Code Review**: References are validated for accuracy and helpfulness
- **Documentation Updates**: Code references are updated when docs change
- **Release Preparation**: Link validation included in pre-release quality checks

This comprehensive linking system ensures that the Bee Organized codebase remains maintainable, understandable, and connected to its business and architectural context throughout its evolution.