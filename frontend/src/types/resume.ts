export interface ResumeDocument {
name: string;
headline: string;

professional_summary?: {
content: string;
};

technical_skills?: {
categories: {
category: string;
skills: string[];
}[];
};

professional_experience?: any[];

certifications?: any[];

education?: any[];
}
