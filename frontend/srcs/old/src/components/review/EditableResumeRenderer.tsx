// import { forwardRef } from "react";

// import InlineEditableText from "./InlineEditableText";
// import ResumeSection from "../resume/ResumeSection";

// interface Props {
//   runId: string;
//   resume: any;
//   onEdited: () => void;
// }

// const EditableResumeRenderer = forwardRef<HTMLDivElement, Props>(
//   ({ runId, resume, onEdited }, ref) => {
//     if (!resume) {
//       return null;
//     }

//     return (
//       <div
//         ref={ref}
//         id="resume-pdf-target"
//         className="
//         bg-white
//         border
//         shadow-xl
//         rounded-xl
//         p-10
//         text-sm
//         leading-6
//         h-full
//       "
//       >
//         {/* Header */}

//         <div className="text-center mb-6">
//           <h1 className="text-3xl font-bold tracking-wide">{resume.name}</h1>

//           <div className="mt-2 flex justify-center">
//             <InlineEditableText
//               runId={runId}
//               path="headline"
//               value={resume.headline || ""}
//               onSaved={onEdited}
//               className="text-gray-600 font-medium"
//             />
//           </div>

//           <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
//             <span>{resume.contact_info?.location}</span>
//             <span>|</span>
//             <span>{resume.contact_info?.phone}</span>
//             <span>|</span>
//             <span>{resume.contact_info?.email}</span>
//           </div>
//         </div>

//         <ResumeSection title="Professional Summary">
//           <InlineEditableText
//             runId={runId}
//             path="professional_summary.content"
//             value={resume.professional_summary?.content || ""}
//             onSaved={onEdited}
//             multiline
//             className="text-gray-700 block w-full"
//           />
//         </ResumeSection>

//         <ResumeSection title="Technical Skills">
//           <div className="space-y-2">
//             {resume.technical_skills?.categories?.map(
//               (category: any, ci: number) => (
//                 <div key={category.category}>
//                   <span className="font-semibold">{category.category}:</span>{" "}
//                   <InlineEditableText
//                     runId={runId}
//                     path={`technical_skills.categories.${ci}.skills`}
//                     value={category.skills.join(", ")}
//                     onSaved={onEdited}
//                     className="text-gray-700"
//                     serialize={(text: string) =>
//                       text
//                         .split(",")
//                         .map((s) => s.trim())
//                         .filter(Boolean)
//                     }
//                   />
//                 </div>
//               ),
//             )}
//           </div>
//         </ResumeSection>

//         <ResumeSection title="Professional Experience">
//           {resume.professional_experience?.map((exp: any, ei: number) => (
//             <div key={ei} className="mb-8">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="font-bold text-base">{exp.role}</h3>
//                   <div className="text-gray-600">{exp.company}</div>
//                 </div>

//                 <div className="text-gray-500 text-xs">
//                   {exp.start_date} - {exp.end_date}
//                 </div>
//               </div>

//               <ul className="list-disc ml-5 mt-3 space-y-1">
//                 {exp.responsibilities?.map((point: string, ri: number) => (
//                   <li key={ri}>
//                     <InlineEditableText
//                       runId={runId}
//                       path={`professional_experience.${ei}.responsibilities.${ri}`}
//                       value={point}
//                       onSaved={onEdited}
//                     />
//                   </li>
//                 ))}
//               </ul>

//               {exp.projects?.length > 0 && (
//                 <div className="mt-4 ml-2">
//                   {exp.projects.map((project: any, pi: number) => (
//                     <div key={pi} className="mb-4">
//                       <h4 className="font-semibold">{project.title}</h4>

//                       <ul className="list-disc ml-5 mt-1">
//                         {project.bullet_points?.map(
//                           (bullet: string, bi: number) => (
//                             <li key={bi}>
//                               <InlineEditableText
//                                 runId={runId}
//                                 path={`professional_experience.${ei}.projects.${pi}.bullet_points.${bi}`}
//                                 value={bullet}
//                                 onSaved={onEdited}
//                               />
//                             </li>
//                           ),
//                         )}
//                       </ul>
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>
//           ))}
//         </ResumeSection>

//         <ResumeSection title="Certifications">
//           <ul className="list-disc ml-5">
//             {resume.certifications?.map((cert: any, index: number) => (
//               <li key={index}>{cert.name}</li>
//             ))}
//           </ul>
//         </ResumeSection>

//         <ResumeSection title="Education">
//           {resume.education?.map((edu: any, index: number) => (
//             <div key={index} className="mb-2">
//               <div className="font-semibold">{edu.degree}</div>

//               <div>{edu.institution}</div>

//               <div className="text-gray-500 text-sm">
//                 {edu.start_year} - {edu.end_year}
//               </div>
//             </div>
//           ))}
//         </ResumeSection>
//       </div>
//     );
//   },
// );

// EditableResumeRenderer.displayName = "EditableResumeRenderer";

// export default EditableResumeRenderer;

/**seond */
// import { forwardRef } from "react";

// import InlineEditableText from "./InlineEditableText";
// import ResumeSection from "../resume/ResumeSection";

// interface Props {
//   runId: string;
//   resume: any;
//   onEdited: () => void;
// }

// const EditableResumeRenderer = forwardRef<HTMLDivElement, Props>(
//   ({ runId, resume, onEdited }, ref) => {
//     if (!resume) {
//       return null;
//     }

//     return (
//       <div
//         ref={ref}
//         id="resume-pdf-target"
//         className="
//           bg-white
//           border
//           shadow-xl
//           rounded-xl
//           p-10
//           text-sm
//           leading-6
//           h-full
//         "
//       >
//         {/* Header */}

//         <div className="text-center mb-6">
//           <h1 className="text-3xl font-bold tracking-wide">{resume.name}</h1>

//           <div className="mt-2 flex justify-center">
//             <InlineEditableText
//               runId={runId}
//               path="headline"
//               value={resume.headline || ""}
//               onSaved={onEdited}
//               className="text-gray-600 font-medium"
//             />
//           </div>

//           <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
//             <span>{resume.contact_info?.location}</span>
//             <span>|</span>
//             <span>{resume.contact_info?.phone}</span>
//             <span>|</span>
//             <span>{resume.contact_info?.email}</span>
//           </div>
//         </div>

//         <ResumeSection title="Professional Summary">
//           <InlineEditableText
//             runId={runId}
//             path="professional_summary.content"
//             value={resume.professional_summary?.content || ""}
//             onSaved={onEdited}
//             multiline
//             className="text-gray-700 block w-full"
//           />
//         </ResumeSection>

//         <ResumeSection title="Technical Skills">
//           <div className="space-y-2">
//             {resume.technical_skills?.categories?.map(
//               (category: any, ci: number) => (
//                 <div key={category.category}>
//                   <span className="font-semibold">{category.category}:</span>{" "}
//                   <InlineEditableText
//                     runId={runId}
//                     path={`technical_skills.categories.${ci}.skills`}
//                     value={category.skills.join(", ")}
//                     onSaved={onEdited}
//                     className="text-gray-700"
//                     serialize={(text: string) =>
//                       text
//                         .split(",")
//                         .map((s) => s.trim())
//                         .filter(Boolean)
//                     }
//                   />
//                 </div>
//               ),
//             )}
//           </div>
//         </ResumeSection>

//         <ResumeSection title="Professional Experience">
//           {resume.professional_experience?.map((exp: any, ei: number) => (
//             <div key={ei} className="mb-8">
//               <div className="flex justify-between items-start">
//                 <div>
//                   <h3 className="font-bold text-base">{exp.role}</h3>

//                   <div className="text-gray-600">{exp.company}</div>
//                 </div>

//                 <div className="text-gray-500 text-xs">
//                   {exp.start_date} - {exp.end_date}
//                 </div>
//               </div>

//               <ul className="list-disc ml-5 mt-3 space-y-1">
//                 {exp.responsibilities?.map((point: string, ri: number) => (
//                   <li key={ri}>
//                     <InlineEditableText
//                       runId={runId}
//                       path={`professional_experience.${ei}.responsibilities.${ri}`}
//                       value={point}
//                       onSaved={onEdited}
//                     />
//                   </li>
//                 ))}
//               </ul>

//               {exp.projects?.length > 0 && (
//                 <div className="mt-4 ml-2">
//                   {exp.projects.map((project: any, pi: number) => (
//                     <div key={pi} className="mb-4">
//                       <h4 className="font-semibold">{project.title}</h4>

//                       <ul className="list-disc ml-5 mt-1">
//                         {project.bullet_points?.map(
//                           (bullet: string, bi: number) => (
//                             <li key={bi}>
//                               <InlineEditableText
//                                 runId={runId}
//                                 path={`professional_experience.${ei}.projects.${pi}.bullet_points.${bi}`}
//                                 value={bullet}
//                                 onSaved={onEdited}
//                               />
//                             </li>
//                           ),
//                         )}
//                       </ul>
//                     </div>
//                   ))}
//                 </div>
//               )}
//             </div>
//           ))}
//         </ResumeSection>

//         <ResumeSection title="Certifications">
//           <ul className="list-disc ml-5">
//             {resume.certifications?.map((cert: any, index: number) => (
//               <li key={index}>{cert.name}</li>
//             ))}
//           </ul>
//         </ResumeSection>

//         <ResumeSection title="Education">
//           {resume.education?.map((edu: any, index: number) => (
//             <div key={index} className="mb-2">
//               <div className="font-semibold">{edu.degree}</div>

//               <div>{edu.institution}</div>

//               <div className="text-gray-500 text-sm">
//                 {edu.start_year} - {edu.end_year}
//               </div>
//             </div>
//           ))}
//         </ResumeSection>
//       </div>
//     );
//   },
// );

// EditableResumeRenderer.displayName = "EditableResumeRenderer";

// export default EditableResumeRenderer;

import { forwardRef } from "react";

import InlineEditableText from "./InlineEditableText";
import ResumeSection from "../resume/ResumeSection";

interface Props {
  runId: string;
  resume: any;
  originalResume?: any;
  onEdited: () => void;
}

const EditableResumeRenderer = forwardRef<HTMLDivElement, Props>(
  ({ runId, resume, originalResume, onEdited }, ref) => {
    if (!resume) {
      return null;
    }

    return (
      // AFTER
      <div
        ref={ref}
        id="resume-pdf-target"
        className="
          bg-white
          border border-gray-200
          shadow-sm
          rounded-xl
          p-6 sm:p-8 lg:p-10
          text-sm
          leading-6
          h-full
          min-w-0
        "
      >
        {/* Header */}

        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold tracking-wide">{resume.name}</h1>

          <div className="mt-2 flex justify-center">
            <InlineEditableText
              runId={runId}
              path="headline"
              value={resume.headline || ""}
              originalValue={originalResume?.headline || ""}
              onSaved={onEdited}
              className="text-gray-600 font-medium"
            />
          </div>

          <div className="mt-3 text-gray-500 text-xs flex flex-wrap justify-center gap-2">
            <span>{resume.contact_info?.location}</span>
            <span>|</span>
            <span>{resume.contact_info?.phone}</span>
            <span>|</span>
            <span>{resume.contact_info?.email}</span>
          </div>
        </div>

        <ResumeSection title="Professional Summary">
          <InlineEditableText
            runId={runId}
            path="professional_summary.content"
            value={resume.professional_summary?.content || ""}
            originalValue={originalResume?.professional_summary?.content || ""}
            onSaved={onEdited}
            multiline
            className="text-gray-700 block w-full"
          />
        </ResumeSection>

        <ResumeSection title="Technical Skills">
          <div className="space-y-2">
            {resume.technical_skills?.categories?.map(
              (category: any, ci: number) => {
                const originalCategory =
                  originalResume?.technical_skills?.categories?.find(
                    (c: any) => c.category === category.category,
                  );

                return (
                  <div key={category.category}>
                    <span className="font-semibold">{category.category}:</span>{" "}
                    <InlineEditableText
                      runId={runId}
                      path={`technical_skills.categories.${ci}.skills`}
                      value={category.skills.join(", ")}
                      originalValue={originalCategory?.skills?.join(", ") || ""}
                      onSaved={onEdited}
                      className="text-gray-700"
                      serialize={(text: string) =>
                        text
                          .split(",")
                          .map((s) => s.trim())
                          .filter(Boolean)
                      }
                    />
                  </div>
                );
              },
            )}
          </div>
        </ResumeSection>

        <ResumeSection title="Professional Experience">
          {resume.professional_experience?.map((exp: any, ei: number) => {
            const originalExp = originalResume?.professional_experience?.find(
              (e: any) => e.company === exp.company || e.role === exp.role,
            );

            return (
              <div key={ei} className="mb-8">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-base">
                      <InlineEditableText
                        runId={runId}
                        path={`professional_experience.${ei}.role`}
                        value={exp.role || ""}
                        originalValue={originalExp?.role || ""}
                        onSaved={onEdited}
                      />
                    </h3>

                    <div className="text-gray-600">
                      <InlineEditableText
                        runId={runId}
                        path={`professional_experience.${ei}.company`}
                        value={exp.company || ""}
                        originalValue={originalExp?.company || ""}
                        onSaved={onEdited}
                      />
                    </div>
                  </div>

                  <div className="text-gray-500 text-xs">
                    <InlineEditableText
                      runId={runId}
                      path={`professional_experience.${ei}.duration`}
                      value={`${exp.start_date} - ${exp.end_date}`}
                      originalValue={`${originalExp?.start_date ?? ""} - ${originalExp?.end_date ?? ""}`}
                      onSaved={onEdited}
                      serialize={(text) => {
                        const parts = text.split("-").map((s) => s.trim());

                        return {
                          start_date: parts[0] ?? "",
                          end_date: parts[1] ?? "",
                        };
                      }}
                    />
                  </div>
                </div>

                <ul className="list-disc ml-5 mt-3 space-y-2">
                  {exp.responsibilities?.map((point: string, ri: number) => (
                    <li key={ri}>
                      <InlineEditableText
                        runId={runId}
                        path={`professional_experience.${ei}.responsibilities.${ri}`}
                        value={point}
                        originalValue={
                          originalExp?.responsibilities?.[ri] || ""
                        }
                        onSaved={onEdited}
                      />
                    </li>
                  ))}
                </ul>

                {exp.projects?.length > 0 && (
                  <div className="mt-4 ml-2">
                    {exp.projects.map((project: any, pi: number) => {
                      const originalProject = originalExp?.projects?.find(
                        (p: any) => p.title === project.title,
                      );

                      return (
                        <div key={pi} className="mb-4">
                          <h4 className="font-semibold">
                            <InlineEditableText
                              runId={runId}
                              path={`professional_experience.${ei}.projects.${pi}.title`}
                              value={project.title || ""}
                              originalValue={originalProject?.title || ""}
                              onSaved={onEdited}
                            />
                          </h4>

                          <ul className="list-disc ml-5 mt-2 space-y-1">
                            {project.bullet_points?.map(
                              (bullet: string, bi: number) => (
                                <li key={bi}>
                                  <InlineEditableText
                                    runId={runId}
                                    path={`professional_experience.${ei}.projects.${pi}.bullet_points.${bi}`}
                                    value={bullet}
                                    originalValue={
                                      originalProject?.bullet_points?.[bi] || ""
                                    }
                                    onSaved={onEdited}
                                  />
                                </li>
                              ),
                            )}
                          </ul>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          })}
        </ResumeSection>
        <ResumeSection title="Certifications">
          <ul className="list-disc ml-5 space-y-1">
            {resume.certifications?.map((cert: any, index: number) => (
              <li key={index}>
                <InlineEditableText
                  runId={runId}
                  path={`certifications.${index}.name`}
                  value={cert.name || ""}
                  originalValue={
                    originalResume?.certifications?.[index]?.name || ""
                  }
                  onSaved={onEdited}
                />
              </li>
            ))}
          </ul>
        </ResumeSection>

        <ResumeSection title="Education">
          {resume.education?.map((edu: any, index: number) => {
            const originalEdu = originalResume?.education?.[index];

            return (
              <div key={index} className="mb-4">
                <div className="font-semibold">
                  <InlineEditableText
                    runId={runId}
                    path={`education.${index}.degree`}
                    value={edu.degree || ""}
                    originalValue={originalEdu?.degree || ""}
                    onSaved={onEdited}
                  />
                </div>

                <div>
                  <InlineEditableText
                    runId={runId}
                    path={`education.${index}.institution`}
                    value={edu.institution || ""}
                    originalValue={originalEdu?.institution || ""}
                    onSaved={onEdited}
                  />
                </div>

                <div className="text-gray-500 text-sm">
                  <InlineEditableText
                    runId={runId}
                    path={`education.${index}.duration`}
                    value={`${edu.start_year} - ${edu.end_year}`}
                    originalValue={`${originalEdu?.start_year ?? ""} - ${originalEdu?.end_year ?? ""}`}
                    onSaved={onEdited}
                    serialize={(text) => {
                      const parts = text.split("-").map((s) => s.trim());

                      return {
                        start_year: parts[0] ?? "",
                        end_year: parts[1] ?? "",
                      };
                    }}
                  />
                </div>
              </div>
            );
          })}
        </ResumeSection>
      </div>
    );
  },
);

EditableResumeRenderer.displayName = "EditableResumeRenderer";

export default EditableResumeRenderer;
