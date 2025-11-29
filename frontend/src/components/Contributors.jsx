const team = [
  {
    name: "Ranjith Perumal",
    role: "Full Stack AI Developer",
    img: "https://avatar.iran.liara.run/username?username=Ranjith+Perumal",
    desc: "Architecting solutions, AI development, etc.",
    hobbies: "Travelling, Exploring new tech and Swimming."
  },
  {
    name: "Vivek Sharma",
    role: "Full Stack AI Developer",
    img: "https://avatar.iran.liara.run/username?username=Vivek+Sharma",
    desc: "Nvidia certified agentic AI professional, building full stack solutions.",
    hobbies: "Playing PC Games, Outdoor sports and Photography."
  },
  {
    name: "Harsh Sinha",
    role: "Platform Engineer",
    img: "https://avatar.iran.liara.run/username?username=Harsh+Sinha",
    desc: "Specializes in ML-OPs deployments, building CI/CD pipelines, etc.",
    hobbies: "Playing PC Games.",
  },
  {
    name: "Ameya Kirtikar",
    role: "Full Stack AI Developer",
    img: "https://avatar.iran.liara.run/username?username=Ameya+Kirtikar",
    desc: "Specializes in full stack development.",
    hobbies: "Trekking, Swimming and Football.",
  },
];

export default function Contributors() {
  return (
    <div className="w-full px-10 py-12 text-white">
      <h2 className="text-4xl font-bold mb-10">Contributors</h2>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {team.map((member, index) => (
          <div
            key={index}
            className="flex flex-col sm:flex-row gap-6 bg-gray-900 p-6 rounded-xl border border-gray-700 hover:border-blue-500 transition"
          >
            {/* Photo */}
            <img
              src={member.img}
              alt={member.name}
              className="w-32 h-32 object-cover rounded-xl"
            />

            {/* Text */}
            <div>
              <h3 className="text-2xl font-semibold">{member.name}</h3>
              <p className="text-blue-400">{member.role}</p>
              <p className="mt-3 text-gray-300">{member.desc}</p>
              <p className="mt-3 text-gray-300"><span className="font-semibold">Hobbies:</span> {member.hobbies}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
