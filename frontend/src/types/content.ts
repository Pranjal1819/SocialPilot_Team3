export type ContentType = "text" | "image" | "video" | "carousel" | "story" | "reel";
export type PostStatus = "draft" | "scheduled" | "queued" | "published";
export type RecurringFrequency = "none" | "daily" | "weekly" | "monthly";

export interface ScheduledPost {
  id: string;
  title?: string;
  caption: string;
  contentType: ContentType;
  platforms: string[];
  scheduledDate: string;
  scheduledTime: string;
  status: PostStatus;
  recurring: RecurringFrequency;
  campaign?: string;
  tags?: string[];
  mediaUrls: string[]; // object URLs for uploaded media (images/video/carousel/story/reel)
}
