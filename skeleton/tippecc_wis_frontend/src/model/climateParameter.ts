/**
 * Generated by orval v6.25.0 🍺
 * Do not edit manually.
 * Tippecc WIS
 * Tippecc WIS is a web-based information system in development with a generic workflow for climate indices calculation
 * OpenAPI spec version: 1.0.0
 */

export interface ClimateParameter {
  datatype: string;
  desc: string;
  input_list: string[];
  name: string;
  /** True if parameter is optional */
  readonly optional: boolean;
  unit_list: string[];
}
