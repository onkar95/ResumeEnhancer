import type { ResumeDocument } from "./resume";


export interface WorkflowResponse {
parsed_resume: ResumeDocument;
tailored_resume: ResumeDocument;

gap_analysis: any;
enhancement_plan: any;
validation_result: any;
comparison_data: any;
}
