import {Comment, CommentReply} from './state';

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
        let url = `${this.baseUrl}/comments/`;
        let method = 'POST';

        if (comment.remoteId) {
            url = `${this.baseUrl}/comments/${comment.remoteId}/`;
            method = 'PUT';
        }

        let response = await fetch(url, {
            method,
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

    async saveCommentReply(comment: Comment, reply: CommentReply) {
        let url = `${this.baseUrl}/comments/${comment.remoteId}/replies/`;
        let method = 'POST';

        if (reply.remoteId) {
            url = `${this.baseUrl}/comments/${comment.remoteId}/replies/${reply.remoteId}/`;
            method = 'PUT';
        }

        let response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-Review-Token': this.reviewToken,
            },
            body: JSON.stringify({
                'text': reply.text,
            }),
        });

        return await response.json();
    }
}
