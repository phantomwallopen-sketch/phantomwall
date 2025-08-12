// PhantomWall JS SDK (stub)
export function guard(prompt, policy = "strict") {
    const blocked = ["ignore previous", "disregard all", "override instructions"];
    const lowerPrompt = prompt.toLowerCase();
    for (let word of blocked) {
        if (lowerPrompt.includes(word)) {
            return { error: "Prompt blocked by PhantomWall SDK." };
        }
    }
    return { prompt };
}
