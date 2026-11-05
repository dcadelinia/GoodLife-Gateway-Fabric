import { PrismaClient } from "@prisma/client";
const prisma = new PrismaClient();

const courses = [
  { slug: "future-tech-basics", title: "Future Technology Basics", category: "Future Technology Basics", level: "youth", ageMin: 10, ageMax: 14, description: "Foundational concepts in emerging technology for younger learners." },
  { slug: "ai-literacy", title: "AI Literacy", category: "AI Literacy", level: "high-school", ageMin: 14, ageMax: 18, description: "Responsible understanding of AI systems, capabilities, and limits." },
  { slug: "logistics-fundamentals", title: "Logistics & Supply-Chain Fundamentals", category: "Logistics and Supply-Chain Fundamentals", level: "college", ageMin: 16, ageMax: 25, description: "Regional logistics coordination and supply-chain basics." },
  { slug: "coding-data-skills", title: "Coding and Data Skills", category: "Coding and Data Skills", level: "high-school", description: "Practical coding and data literacy pathways." },
  { slug: "entrepreneurship", title: "Entrepreneurship", category: "Entrepreneurship", level: "college", description: "Building ventures with ethical client acquisition practices." },
  { slug: "career-pathways", title: "Career Pathways", category: "Career Pathways", level: "high-school", description: "Career readiness for technology and logistics roles." },
  { slug: "college-readiness", title: "College and Professional Readiness", category: "College and Professional Readiness", level: "high-school", description: "Preparation for higher education and workforce entry." },
];

async function main() {
  for (const c of courses) {
    const course = await prisma.course.upsert({
      where: { slug: c.slug },
      create: { ...c, isPublished: true },
      update: { title: c.title, description: c.description, isPublished: true },
    });
    const existing = await prisma.lesson.count({ where: { courseId: course.id } });
    if (existing === 0) {
      await prisma.lesson.createMany({
        data: [
          { courseId: course.id, title: "Introduction", content: `Welcome to ${c.title}. Learning objectives and safety notes.`, order: 1, durationMin: 15 },
          { courseId: course.id, title: "Core Concepts", content: `Key ideas in ${c.category}.`, order: 2, durationMin: 25 },
          { courseId: course.id, title: "Practice Project", content: "Hands-on activity. Parent/educator supervision recommended for minors.", order: 3, durationMin: 30 },
        ],
      });
    }
  }
  console.log("Seeded Learning Lab curriculum");
}

main().finally(() => prisma.$disconnect());
