interface Props {
  projects: any[];
}

export default function ResumeProjects({ projects }: Props) {
  if (!projects?.length) return null;

  return (
    <>
      {projects.map((project, index) => (
        <div key={index} className="mb-5">
          {" "}
          <h3 className="font-semibold">{project.title} </h3>
          ```
          <ul className="list-disc ml-5 mt-2">
            {project.bullet_points?.map((point: string, idx: number) => (
              <li key={idx}>{point}</li>
            ))}
          </ul>
        </div>
      ))}
    </>
  );
}
