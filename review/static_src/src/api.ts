import {Comment} from './state';

export default class APIClient {
    baseUrl: string;
    reviewToken: string;

    constructor(baseUrl: string, reviewToken: string) {
        this.baseUrl = baseUrl;
        this.reviewToken = reviewToken;
    }

    async fetchAllComments() {
        let response = await fetch(`${this.baseUrl}/comments/`, {
            headers: {
                'X-Review-Token': this.reviewToken,
            }
        });

        return await response.json();
    }

    async saveComment(comment: Comment) {
        // TODO: PUT if has remote id

        let response = await fetch(`${this.baseUrl}/comments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Review-Token': this.reviewToken,
            },
            body: JSON.stringify({
                'quote': comment.annotation.annotation.quote,
                'text': comment.text,
                'is_resolved': false,
                'content_path': comment.annotation.contentPath,
                'start_xpath': comment.annotation.annotation.ranges[0].start || '.',
                'start_offset': comment.annotation.annotation.ranges[0].startOffset,
                'end_xpath': comment.annotation.annotation.ranges[0].end || '.',
                'end_offset': comment.annotation.annotation.ranges[0].endOffset,
            }),
        });

        return await response.json();
    }

    async deleteComment(comment: Comment) {
        if (comment.remoteId) {
            await fetch(`${this.baseUrl}/comments/${comment.remoteId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Review-Token': this.reviewToken,
                },
            });
        }
    }
}
