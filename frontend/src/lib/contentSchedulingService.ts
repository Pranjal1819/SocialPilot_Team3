import { ScheduledPost } from "@/types/content";

let posts: ScheduledPost[] = [];
const delay = () => new Promise((resolve) => setTimeout(resolve, 160));

/** Mock client-side contract. Replace internals with the future API client without changing consuming UI. */
export async function getScheduledPosts(): Promise<ScheduledPost[]> { await delay(); return [...posts]; }
export async function saveScheduledPost(post: ScheduledPost): Promise<ScheduledPost> { await delay(); posts = [...posts.filter((item) => item.id !== post.id), post]; return post; }
export async function deleteScheduledPost(id: string): Promise<void> { await delay(); posts = posts.filter((post) => post.id !== id); }
export async function duplicateScheduledPost(post: ScheduledPost): Promise<ScheduledPost> {
  await delay();
  const duplicate = { ...post, id: `${Date.now()}`, title: `${post.title || "Untitled post"} (copy)`, status: "draft" as const };
  posts = [...posts, duplicate];
  return duplicate;
}
