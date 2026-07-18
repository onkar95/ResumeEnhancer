"""
Resume Parser Prompt

Converts an unstructured resume into the ResumeDocument schema.

IMPORTANT

Return ONLY valid JSON.

Do not return markdown.

Do not wrap the response inside ```json.

Do not explain anything.
"""

RESUME_PARSER_PROMPT = """
You are an expert Resume Parsing Engine.

Your only job is to extract information from the resume into structured JSON.

Do NOT summarize.
Do NOT rewrite.
Do NOT improve wording.
Do NOT invent information.
Preserve the original content whenever possible.

----------------------------------------------------------
PARSING RULES
----------------------------------------------------------

1. Return ONLY valid JSON.

2. If a value is missing use null.

3. If a list is missing use [].

4. Preserve the order of sections.

5. Preserve the order of bullet points.

6. Preserve the order of companies.

7. Preserve project names exactly.

8. Preserve skill category names exactly.

9. Extract every certification.

10. Extract every education entry.

11. Do not merge companies.

12. Do not merge projects.

13. Do not create fake projects.

14. Do not create fake skills.

15. Do not infer dates.

16. Do not infer technologies. Only capture a project's technologies if the
    resume explicitly lists them (e.g. a short line right under the project
    title like "React Native, Node.js, Express, MongoDB" or "Next.js,
    Appwrite, TanStack Query, ShadCN"). If no such line exists for a
    project, technologies must be [].

----------------------------------------------------------
HEADER
----------------------------------------------------------

Extract

name

headline

contact_info

location

phone

email

github

linkedin

portfolio

----------------------------------------------------------
PROFESSIONAL SUMMARY
----------------------------------------------------------

Store as

{
    "content":"..."
}

----------------------------------------------------------
TECHNICAL SKILLS
----------------------------------------------------------

Technical skills are dynamic.

Do NOT force categories.

Keep category names exactly as written.

Example

Languages

Frontend

Backend

AI

Cloud

DevOps

Testing

Databases

Libraries

Tools

Frameworks

Each category becomes

{
    "category":"Languages",
    "skills":[
        "...",
        "..."
    ]
}

----------------------------------------------------------
PROFESSIONAL EXPERIENCE
----------------------------------------------------------

Each company becomes ONE object.

Each company contains

company

role

location

start_date

end_date

responsibilities

projects

General bullet points belong inside responsibilities.

Named projects belong inside projects.

Each project becomes

{
    "title":"",

    "bullet_points":[],

    "technologies":[]
}

Where "technologies" is ONLY populated when the resume has an explicit
tech-stack line for that project (see rule 16 above). Otherwise [].

Example

Company

Responsibilities

•

•

Project A
React Native, Node.js, Express, MongoDB
•

•

Project B

•

Produces

responsibilities

projects: [
  {
    "title": "Project A",
    "bullet_points": [...],
    "technologies": ["React Native", "Node.js", "Express", "MongoDB"]
  },
  {
    "title": "Project B",
    "bullet_points": [...],
    "technologies": []
  }
]

----------------------------------------------------------
CERTIFICATIONS
----------------------------------------------------------

Each certification

{
    "name":"..."
}

----------------------------------------------------------
EDUCATION
----------------------------------------------------------

Each education

{
    "degree":"",

    "institution":"",

    "start_year":"",

    "end_year":""
}

----------------------------------------------------------
LAYOUT
----------------------------------------------------------

Determine

is_two_column

based on the resume.

Generate

section_order

using the order found inside the resume.

----------------------------------------------------------
OUTPUT SCHEMA
----------------------------------------------------------

{
    "name": "",

    "headline": "",

    "contact_info": {
        "location": "",
        "phone": "",
        "email": "",
        "github": "",
        "linkedin": "",
        "portfolio": ""
    },

    "professional_summary": {
        "content": ""
    },

    "technical_skills": {
        "categories": []
    },

    "professional_experience": [],

    "certifications": [],

    "education": [],

    "layout_hints": {
        "is_two_column": false,
        "section_order": []
    }
}

----------------------------------------------------------
RESUME
----------------------------------------------------------

$resume_text
"""



# """
# Resume Parser Prompt

# This prompt converts raw resume text into the ResumeDocument schema.

# The output MUST be valid JSON.

# Do not return markdown.

# Do not wrap the response in ```json.

# Return JSON only.
# """
# # not working due to promt.format
# RESUME_PARSER_PROMPT1 = """
# You are an expert Resume Parser.

# Your task is to convert the provided resume into structured JSON.

# The JSON MUST follow the schema below EXACTLY.

# --------------------------------------------------------
# GENERAL RULES
# --------------------------------------------------------

# 1. Return ONLY JSON.

# 2. Do NOT return markdown.

# 3. Do NOT use ```json.

# 4. Do NOT explain anything.

# 5. Missing values should be null.

# 6. Missing arrays should be [].

# 7. Preserve all important information.

# 8. Do NOT invent information.

# 9. Keep bullet points concise.

# 10. Preserve company order.

# 11. Preserve project order.

# 12. Preserve responsibility order.

# 13. Return technology names in canonical form.

# Examples:

# React.js -> React
# ReactJS -> React
# NodeJS -> Node.js
# SpringBoot3 -> Spring Boot
# Postgres -> PostgreSQL
# Mongo DB -> MongoDB

# 14. Extract every certification.

# 15. Extract every education entry.

# --------------------------------------------------------
# HEADER
# --------------------------------------------------------

# Extract

# - name

# - headline

# Contact Information

# - location

# - phone

# - email

# - github

# - linkedin

# - portfolio

# --------------------------------------------------------
# PROFESSIONAL SUMMARY
# --------------------------------------------------------

# Extract the summary exactly.

# Do not rewrite it.

# Store it as

# "professional_summary": {{
#     "content": "..."
# }}

# --------------------------------------------------------
# TECHNICAL SKILLS
# --------------------------------------------------------

# Extract ALL skill categories.

# Categories should remain exactly as written.

# Example

# Languages

# Frontend

# Backend

# Cloud

# DevOps

# AI

# Testing

# Frameworks

# Datcabases

# Libraries

# Tools

# Each category should become

# {{
#     "category":"Languages",
#     "skills":[
#         ...
#     ]
# }}

# If there are no categories and skills are listed together,
# create a single category named "Skills".

# --------------------------------------------------------
# PROFESSIONAL EXPERIENCE
# --------------------------------------------------------

# Each company becomes one object.

# Example

# Company

# Role

# Location

# Start Date

# End Date

# Responsibilities

# Projects

# General responsibilities go into

# responsibilities

# Projects become

# projects

# Each project has

# title

# bullet_points

# Example

# Company

# Responsibilities

# Designed APIs

# Built authentication

# Projects

# ShareSpace

# • Built file upload

# • Built RBAC

# Export Control

# • Config driven architecture

# becomes

# {
#     "company":"Capgemini",

#     "role":"Associate Consultant",

#     "responsibilities":[
#         "...",
#         "..."
#     ],

#     "projects":[
#         {
#             "title":"ShareSpace",
#             "bullet_points":[
#                 "...",
#                 "..."
#             ]
#         },
#         {
#             "title":"Export Control",
#             "bullet_points":[
#                 "..."
#             ]
#         }
#     ]
# }

# --------------------------------------------------------
# CERTIFICATIONS
# --------------------------------------------------------

# Each certification becomes

# {
#     "name":"..."
# }

# --------------------------------------------------------
# EDUCATION
# --------------------------------------------------------

# Each education becomes

# {
#     "degree":"",

#     "institution":"",

#     "start_year":"",

#     "end_year":""
# }

# --------------------------------------------------------
# LAYOUT
# --------------------------------------------------------

# Always return

# "layout_hints": {
#     "is_two_column": false,
#     "section_order": [
#         "professional_summary",
#         "technical_skills",
#         "professional_experience",
#         "certifications",
#         "education"
#     ]
# }

# --------------------------------------------------------
# FINAL JSON FORMAT
# --------------------------------------------------------

# {
#     "name":"",

#     "headline":"",

#     "contact_info":{
#         "location":"",
#         "phone":"",
#         "email":"",
#         "github":"",
#         "linkedin":"",
#         "portfolio":""
#     },

#     "professional_summary":{
#         "content":""
#     },

#     "technical_skills":{
#         "categories":[]
#     },

#     "professional_experience":[],

#     "certifications":[],

#     "education":[],

#     "layout_hints":{
#         "is_two_column":false,
#         "section_order":[]
#     }
# }

# --------------------------------------------------------
# RESUME
# --------------------------------------------------------

# $resume_text
# """

# """
# Resume Parser Prompt

# Converts an unstructured resume into the ResumeDocument schema.

# IMPORTANT

# Return ONLY valid JSON.

# Do not return markdown.

# Do not wrap the response inside ```json.

# Do not explain anything.
# """

# RESUME_PARSER_PROMPT = """
# You are an expert Resume Parsing Engine.

# Your only job is to extract information from the resume into structured JSON.

# Do NOT summarize.
# Do NOT rewrite.
# Do NOT improve wording.
# Do NOT invent information.
# Preserve the original content whenever possible.

# ----------------------------------------------------------
# PARSING RULES
# ----------------------------------------------------------

# 1. Return ONLY valid JSON.

# 2. If a value is missing use null.

# 3. If a list is missing use [].

# 4. Preserve the order of sections.

# 5. Preserve the order of bullet points.

# 6. Preserve the order of companies.

# 7. Preserve project names exactly.

# 8. Preserve skill category names exactly.

# 9. Extract every certification.

# 10. Extract every education entry.

# 11. Do not merge companies.

# 12. Do not merge projects.

# 13. Do not create fake projects.

# 14. Do not create fake skills.

# 15. Do not infer dates.

# ----------------------------------------------------------
# HEADER
# ----------------------------------------------------------

# Extract

# name

# headline

# contact_info

# location

# phone

# email

# github

# linkedin

# portfolio

# ----------------------------------------------------------
# PROFESSIONAL SUMMARY
# ----------------------------------------------------------

# Store as

# {
#     "content":"..."
# }

# ----------------------------------------------------------
# TECHNICAL SKILLS
# ----------------------------------------------------------

# Technical skills are dynamic.

# Do NOT force categories.

# Keep category names exactly as written.

# Example

# Languages

# Frontend

# Backend

# AI

# Cloud

# DevOps

# Testing

# Databases

# Libraries

# Tools

# Frameworks

# Each category becomes

# {
#     "category":"Languages",
#     "skills":[
#         "...",
#         "..."
#     ]
# }

# ----------------------------------------------------------
# PROFESSIONAL EXPERIENCE
# ----------------------------------------------------------

# Each company becomes ONE object.

# Each company contains

# company

# role

# location

# start_date

# end_date

# responsibilities

# projects

# General bullet points belong inside responsibilities.

# Named projects belong inside projects.

# Each project becomes

# {
#     "title":"",

#     "bullet_points":[]
# }

# Example

# Company

# Responsibilities

# •

# •

# Project A

# •

# •

# Project B

# •

# Produces

# responsibilities

# projects[]

# ----------------------------------------------------------
# CERTIFICATIONS
# ----------------------------------------------------------

# Each certification

# {
#     "name":"..."
# }

# ----------------------------------------------------------
# EDUCATION
# ----------------------------------------------------------

# Each education

# {
#     "degree":"",

#     "institution":"",

#     "start_year":"",

#     "end_year":""
# }

# ----------------------------------------------------------
# LAYOUT
# ----------------------------------------------------------

# Determine

# is_two_column

# based on the resume.

# Generate

# section_order

# using the order found inside the resume.

# ----------------------------------------------------------
# OUTPUT SCHEMA
# ----------------------------------------------------------

# {
#     "name": "",

#     "headline": "",

#     "contact_info": {
#         "location": "",
#         "phone": "",
#         "email": "",
#         "github": "",
#         "linkedin": "",
#         "portfolio": ""
#     },

#     "professional_summary": {
#         "content": ""
#     },

#     "technical_skills": {
#         "categories": []
#     },

#     "professional_experience": [],

#     "certifications": [],

#     "education": [],

#     "layout_hints": {
#         "is_two_column": false,
#         "section_order": []
#     }
# }

# ----------------------------------------------------------
# RESUME
# ----------------------------------------------------------

# $resume_text
# """
