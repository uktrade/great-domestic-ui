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

        return await response.json().then(comments => {
            for (let comment of comments) {
                // Remove the '.' we add when serialising blank xpaths saveComment
                // This seems to confuse annotator.js and causes the annotations
                // to be slightly off
                if (comment.start_xpath == '.') {
                    comment.start_xpath = '';
                }
                if (comment.end_xpath == '.') {
                    comment.end_xpath = '';
                }
            }

            return comments;
        });
    }

    async saveComment(comment: Comment) {
        let url = `${this.baseUrl}/comments/`;
        let method = 'POST';

        if (comment.remoteId) {
            url = `${this.baseUrl}/comments/${comment.remoteId}/`;
            method = 'PUT';
        }

        // TODO: Maybe should PATCH text instead?

        let response = await fetch(url, {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-Review-Token': this.reviewToken,
            },
            body: JSON.stringify({
                'quote': comment.annotation.annotation.quote,
                'text': comment.text,
                'is_resolved': comment.isResolved,  // FIXME: Might blat resolution done by someone else
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

    async saveCommentResolvedStatus(comment: Comment, isResolved: boolean) {
        // Separate endpoint as anyone can mark a comment as resolved
        let method = isResolved ? 'PUT' : 'DELETE';

        await fetch(`${this.baseUrl}/comments/${comment.remoteId}/resolved/`, {
            method,
            headers: {
                'X-Review-Token': this.reviewToken,
            }
        });
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

    async deleteCommentReply(comment: Comment, reply: CommentReply) {
        if (reply.remoteId) {
            await fetch(`${this.baseUrl}/comments/${comment.remoteId}/replies/${reply.remoteId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Review-Token': this.reviewToken,
                },
            });
        }
    }
}
