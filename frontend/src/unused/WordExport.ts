import {
  AlignmentType,
  BorderStyle,
  Document,
  LevelFormat,
  Packer,
  Paragraph,
  TabStopPosition,
  TabStopType,
  TextRun,
} from "docx";

import { saveAs } from "file-saver";

/* =========================================================
   TYPES
========================================================= */

interface ResumeContactInfo {
  location?: string;
  phone?: string;
  email?: string;
  github?: string;
  linkedin?: string;
  portfolio?: string;
}

interface ResumeSkillCategory {
  category?: string;
  skills?: string[];
}

interface ResumeProject {
  title?: string;
  bullet_points?: string[];
}

interface ResumeExperience {
  role?: string;
  company?: string;
  location?: string;
  start_date?: string;
  end_date?: string;
  responsibilities?: string[];
  projects?: ResumeProject[];
}

interface ResumeCertification {
  name?: string;
}

interface ResumeEducation {
  degree?: string;
  institution?: string;
  start_year?: string | number;
  end_year?: string | number;
}

interface ResumeData {
  name?: string;
  headline?: string;

  contact_info?: ResumeContactInfo;

  professional_summary?: {
    content?: string;
  };

  technical_skills?: {
    categories?: ResumeSkillCategory[];
  };

  professional_experience?: ResumeExperience[];

  certifications?: ResumeCertification[];

  education?: ResumeEducation[];
}

/* =========================================================
   DOCUMENT CONSTANTS
========================================================= */

/*
 * Word font sizes are half-points.
 *
 * 22 = 11pt
 * 20 = 10pt
 * 18 = 9pt
 */

const FONT = "Arial";

const BODY_SIZE = 20;
const SMALL_SIZE = 18;
const NAME_SIZE = 30;
const HEADLINE_SIZE = 20;
const SECTION_SIZE = 20;

const PAGE_MARGIN = 720;

/* =========================================================
   HELPERS
========================================================= */

function clean(value?: unknown): string {
  if (value === null || value === undefined) {
    return "";
  }

  return String(value).trim();
}

function hasText(value?: unknown): boolean {
  return clean(value).length > 0;
}

function normalizeDate(value?: string): string {
  const text = clean(value);

  if (!text) {
    return "";
  }

  return text.replace(/\s*-\s*/g, " – ");
}

function formatDateRange(
  start?: string,
  end?: string,
): string {
  const startDate = normalizeDate(start);
  const endDate = normalizeDate(end);

  if (startDate && endDate) {
    return `${startDate} – ${endDate}`;
  }

  return startDate || endDate;
}

function createBodyRun(
  text: string,
  options?: {
    bold?: boolean;
    italics?: boolean;
    size?: number;
  },
): TextRun {
  return new TextRun({
    text,
    font: FONT,
    size: options?.size ?? BODY_SIZE,
    bold: options?.bold ?? false,
    italics: options?.italics ?? false,
  });
}

/* =========================================================
   SECTION HEADING
========================================================= */

function createSectionHeading(
  title: string,
): Paragraph {
  return new Paragraph({
    spacing: {
      before: 180,
      after: 70,
      line: 240,
    },

    border: {
      bottom: {
        color: "000000",
        style: BorderStyle.SINGLE,
        size: 6,
        space: 2,
      },
    },

    children: [
      new TextRun({
        text: title.toUpperCase(),
        bold: true,
        font: FONT,
        size: SECTION_SIZE,
      }),
    ],
  });
}

/* =========================================================
   HEADER
========================================================= */

function createName(
  resume: ResumeData,
): Paragraph {
  return new Paragraph({
    alignment: AlignmentType.CENTER,

    spacing: {
      after: 30,
      line: 240,
    },

    children: [
      new TextRun({
        text: clean(resume.name),
        bold: true,
        font: FONT,
        size: NAME_SIZE,
      }),
    ],
  });
}

function createHeadline(
  resume: ResumeData,
): Paragraph | null {
  const headline = clean(resume.headline);

  if (!headline) {
    return null;
  }

  return new Paragraph({
    alignment: AlignmentType.CENTER,

    spacing: {
      after: 50,
      line: 220,
    },

    children: [
      new TextRun({
        text: headline,
        font: FONT,
        size: HEADLINE_SIZE,
      }),
    ],
  });
}

function createContactLine(
  resume: ResumeData,
): Paragraph | null {
  const contact =
    resume.contact_info || {};

  const parts = [
    clean(contact.location),
    clean(contact.phone),
    clean(contact.email),
    clean(contact.github),
    clean(contact.linkedin),
    clean(contact.portfolio),
  ].filter(Boolean);

  if (!parts.length) {
    return null;
  }

  const children: TextRun[] = [];

  parts.forEach((part, index) => {
    if (index > 0) {
      children.push(
        createBodyRun(" | ", {
          size: SMALL_SIZE,
        }),
      );
    }

    children.push(
      createBodyRun(part, {
        size: SMALL_SIZE,
      }),
    );
  });

  return new Paragraph({
    alignment: AlignmentType.CENTER,

    spacing: {
      after: 90,
      line: 220,
    },

    children,
  });
}

/* =========================================================
   PROFESSIONAL SUMMARY
========================================================= */

function createProfessionalSummary(
  resume: ResumeData,
): Paragraph[] {
  const summary = clean(
    resume.professional_summary?.content,
  );

  if (!summary) {
    return [];
  }

  return [
    createSectionHeading(
      "Professional Summary",
    ),

    new Paragraph({
      alignment: AlignmentType.JUSTIFIED,

      spacing: {
        after: 40,
        line: 240,
      },

      children: [
        createBodyRun(summary),
      ],
    }),
  ];
}

/* =========================================================
   TECHNICAL SKILLS
========================================================= */

function createTechnicalSkills(
  resume: ResumeData,
): Paragraph[] {
  const categories =
    resume.technical_skills?.categories || [];

  const validCategories =
    categories.filter(
      (category) =>
        hasText(category.category) &&
        category.skills?.some(hasText),
    );

  if (!validCategories.length) {
    return [];
  }

  const paragraphs: Paragraph[] = [
    createSectionHeading(
      "Technical Skills",
    ),
  ];

  validCategories.forEach(
    (category) => {
      const skills =
        (category.skills || [])
          .map(clean)
          .filter(Boolean);

      if (!skills.length) {
        return;
      }

      paragraphs.push(
        new Paragraph({
          spacing: {
            after: 20,
            line: 220,
          },

          children: [
            createBodyRun(
              `${clean(category.category)}: `,
              {
                bold: true,
              },
            ),

            createBodyRun(
              `${skills.join(", ")}.`,
            ),
          ],
        }),
      );
    },
  );

  return paragraphs;
}

/* =========================================================
   BULLETS
========================================================= */

function createPrimaryBullet(
  text: string,
): Paragraph {
  return new Paragraph({
    numbering: {
      reference: "resume-primary-bullets",
      level: 0,
    },

    alignment: AlignmentType.JUSTIFIED,

    spacing: {
      after: 25,
      line: 230,
    },

    children: [
      createBodyRun(text),
    ],
  });
}

function createNestedBullet(
  text: string,
): Paragraph {
  return new Paragraph({
    numbering: {
      reference: "resume-nested-bullets",
      level: 0,
    },

    alignment: AlignmentType.JUSTIFIED,

    spacing: {
      after: 15,
      line: 220,
    },

    children: [
      createBodyRun(text),
    ],
  });
}

/* =========================================================
   EXPERIENCE HEADER
========================================================= */

function createExperienceRole(
  experience: ResumeExperience,
): Paragraph | null {
  const role = clean(
    experience.role,
  );

  if (!role) {
    return null;
  }

  return new Paragraph({
    keepNext: true,

    spacing: {
      before: 70,
      after: 15,
      line: 220,
    },

    children: [
      createBodyRun(role, {
        bold: true,
      }),
    ],
  });
}

function createExperienceMeta(
  experience: ResumeExperience,
): Paragraph | null {
  const company = clean(
    experience.company,
  );

  const location = clean(
    experience.location,
  );

  const dateRange =
    formatDateRange(
      experience.start_date,
      experience.end_date,
    );

  const leftParts = [
    company,
    location,
  ].filter(Boolean);

  if (
    !leftParts.length &&
    !dateRange
  ) {
    return null;
  }

  const left =
    leftParts.join(" – ");

  const children: TextRun[] = [];

  if (left) {
    children.push(
      createBodyRun(left),
    );
  }

  if (left && dateRange) {
    children.push(
      createBodyRun(" | "),
    );
  }

  if (dateRange) {
    children.push(
      createBodyRun(dateRange),
    );
  }

  return new Paragraph({
    keepNext: true,

    spacing: {
      after: 45,
      line: 220,
    },

    children,
  });
}

/* =========================================================
   PROJECTS
========================================================= */

function createProject(
  project: ResumeProject,
): Paragraph[] {
  const paragraphs: Paragraph[] = [];

  const title = clean(
    project.title,
  );

  const bullets =
    (project.bullet_points || [])
      .map(clean)
      .filter(Boolean);

  if (!title && !bullets.length) {
    return [];
  }

  if (title) {
    paragraphs.push(
      new Paragraph({
        keepNext:
          bullets.length > 0,

        spacing: {
          before: 45,
          after: 15,
          line: 220,
        },

        children: [
          createBodyRun(
            title,
            {
              bold: true,
            },
          ),
        ],
      }),
    );
  }

  bullets.forEach(
    (bullet) => {
      paragraphs.push(
        createNestedBullet(
          bullet,
        ),
      );
    },
  );

  return paragraphs;
}

/* =========================================================
   PROFESSIONAL EXPERIENCE
========================================================= */

function createProfessionalExperience(
  resume: ResumeData,
): Paragraph[] {
  const experiences =
    resume.professional_experience || [];

  if (!experiences.length) {
    return [];
  }

  const paragraphs: Paragraph[] = [
    createSectionHeading(
      "Professional Experience",
    ),
  ];

  experiences.forEach(
    (experience) => {
      const roleParagraph =
        createExperienceRole(
          experience,
        );

      if (roleParagraph) {
        paragraphs.push(
          roleParagraph,
        );
      }

      const metaParagraph =
        createExperienceMeta(
          experience,
        );

      if (metaParagraph) {
        paragraphs.push(
          metaParagraph,
        );
      }

      const responsibilities =
        (
          experience.responsibilities ||
          []
        )
          .map(clean)
          .filter(Boolean);

      responsibilities.forEach(
        (responsibility) => {
          paragraphs.push(
            createPrimaryBullet(
              responsibility,
            ),
          );
        },
      );

      const projects =
        experience.projects || [];

      if (projects.length) {
        paragraphs.push(
          new Paragraph({
            keepNext: true,

            spacing: {
              before: 50,
              after: 15,
            },

            children: [
              createBodyRun(
                "Key Contributions:",
                {
                  bold: true,
                },
              ),
            ],
          }),
        );

        projects.forEach(
          (project) => {
            paragraphs.push(
              ...createProject(
                project,
              ),
            );
          },
        );
      }
    },
  );

  return paragraphs;
}

/* =========================================================
   CERTIFICATIONS
========================================================= */

function createCertifications(
  resume: ResumeData,
): Paragraph[] {
  const certifications =
    (
      resume.certifications ||
      []
    ).filter(
      (certification) =>
        hasText(
          certification.name,
        ),
    );

  if (!certifications.length) {
    return [];
  }

  const paragraphs: Paragraph[] = [
    createSectionHeading(
      "Certifications",
    ),
  ];

  certifications.forEach(
    (certification) => {
      paragraphs.push(
        createPrimaryBullet(
          clean(
            certification.name,
          ),
        ),
      );
    },
  );

  return paragraphs;
}

/* =========================================================
   EDUCATION
========================================================= */

function createEducation(
  resume: ResumeData,
): Paragraph[] {
  const education =
    resume.education || [];

  if (!education.length) {
    return [];
  }

  const paragraphs: Paragraph[] = [
    createSectionHeading(
      "Education",
    ),
  ];

  education.forEach(
    (item) => {
      const degree = clean(
        item.degree,
      );

      const institution = clean(
        item.institution,
      );

      const startYear = clean(
        item.start_year,
      );

      const endYear = clean(
        item.end_year,
      );

      let dateRange = "";

      if (startYear && endYear) {
        dateRange =
          `${startYear} - ${endYear}`;
      } else {
        dateRange =
          startYear || endYear;
      }

      if (degree) {
        const children: TextRun[] = [
          createBodyRun(
            degree,
            {
              bold: true,
            },
          ),
        ];

        if (dateRange) {
          children.push(
            createBodyRun(
              `\t${dateRange}`,
            ),
          );
        }

        paragraphs.push(
          new Paragraph({
            tabStops: [
              {
                type:
                  TabStopType.RIGHT,
                position:
                  TabStopPosition.MAX,
              },
            ],

            spacing: {
              after: 10,
              line: 220,
            },

            children,
          }),
        );
      }

      if (institution) {
        paragraphs.push(
          new Paragraph({
            spacing: {
              after: 30,
              line: 220,
            },

            children: [
              createBodyRun(
                institution,
              ),
            ],
          }),
        );
      }
    },
  );

  return paragraphs;
}

/* =========================================================
   FILE NAME
========================================================= */

function createFileName(
  resume: ResumeData,
): string {
  const name =
    clean(resume.name) ||
    "resume";

  const safeName =
    name
      .replace(
        /[<>:"/\\|?*]/g,
        "",
      )
      .replace(
        /\s+/g,
        " ",
      )
      .trim();

  return `${safeName}.docx`;
}

/* =========================================================
   DOWNLOAD
========================================================= */

export async function downloadResumeWord(
  resume: ResumeData,
): Promise<void> {
  if (!resume) {
    return;
  }

  const children: Paragraph[] = [];

  /* -------------------------
     Header
  ------------------------- */

  if (hasText(resume.name)) {
    children.push(
      createName(resume),
    );
  }

  const headline =
    createHeadline(resume);

  if (headline) {
    children.push(headline);
  }

  const contactLine =
    createContactLine(resume);

  if (contactLine) {
    children.push(contactLine);
  }

  /* -------------------------
     Sections
  ------------------------- */

  children.push(
    ...createProfessionalSummary(
      resume,
    ),
  );

  children.push(
    ...createTechnicalSkills(
      resume,
    ),
  );

  children.push(
    ...createProfessionalExperience(
      resume,
    ),
  );

  children.push(
    ...createCertifications(
      resume,
    ),
  );

  children.push(
    ...createEducation(
      resume,
    ),
  );

  /* -------------------------
     Document
  ------------------------- */

  const document =
    new Document({
      numbering: {
        config: [
          {
            reference:
              "resume-primary-bullets",

            levels: [
              {
                level: 0,

                format:
                  LevelFormat.BULLET,

                text: "•",

                alignment:
                  AlignmentType.LEFT,

                style: {
                  paragraph: {
                    indent: {
                      left: 360,
                      hanging: 180,
                    },
                  },
                },
              },
            ],
          },

          {
            reference:
              "resume-nested-bullets",

            levels: [
              {
                level: 0,

                format:
                  LevelFormat.BULLET,

                text: "o",

                alignment:
                  AlignmentType.LEFT,

                style: {
                  paragraph: {
                    indent: {
                      left: 720,
                      hanging: 180,
                    },
                  },
                },
              },
            ],
          },
        ],
      },

      styles: {
        default: {
          document: {
            run: {
              font: FONT,
              size: BODY_SIZE,
            },

            paragraph: {
              spacing: {
                after: 0,
                line: 240,
              },
            },
          },
        },
      },

      sections: [
        {
          properties: {
            page: {
              margin: {
                top: PAGE_MARGIN,
                right: PAGE_MARGIN,
                bottom: PAGE_MARGIN,
                left: PAGE_MARGIN,
              },
            },
          },

          children,
        },
      ],
    });

  /* -------------------------
     Generate DOCX
  ------------------------- */

  const blob =
    await Packer.toBlob(
      document,
    );

  saveAs(
    blob,
    createFileName(
      resume,
    ),
  );
}