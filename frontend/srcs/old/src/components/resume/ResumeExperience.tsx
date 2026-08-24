interface Props {
experience: any[];
}

export default function ResumeExperience({
experience,
}: Props) {
if (!experience?.length) return null;

return (
<>
{experience.map((exp, index) => ( <div
       key={index}
       className="mb-6"
     > <div className="flex justify-between"> <h3 className="font-semibold">
{exp.position} </h3>

```
        <span className="text-sm text-gray-500">
          {exp.start_date} - {exp.end_date}
        </span>
      </div>

      <div className="text-gray-600 mb-2">
        {exp.company}
      </div>

      <ul className="list-disc ml-5 space-y-1">
        {exp.bullet_points?.map(
          (
            point: string,
            idx: number
          ) => (
            <li key={idx}>
              {point}
            </li>
          )
        )}
      </ul>
    </div>
  ))}
</>


);
}
