interface Props {
  skills: any;
}

export default function ResumeSkills({ skills }: Props) {
  if (!skills?.categories) return null;

  return (
    <div className="space-y-2">
      {skills.categories.map((category: any) => (
        <div key={category.category}>
          {" "}
          <span className="font-semibold">{category.category}: </span>
        
          <span className="ml-2 text-gray-700">
            {category.skills.join(", ")}
          </span>
        </div>
      ))}
    </div>
  );
}
