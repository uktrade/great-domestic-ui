import APIClient from './api';
import {Annotation} from './annotation';

export class CommentReply {
    text: string;

    constructor(text: string) {
        this.text = text;
    }
}

type CommentState = 'default' | 'creating' | 'editing' | 'saving' | 'deleting' | 'deleted' | 'save_error' | 'delete_error';

export class Comment {
    localId: number;
    annotation: Annotation;
    remoteId: number|null;
    state: CommentState;
    author: string;
    text: string;
    replies: CommentReply[];
    newReply: string;
    _element: HTMLElement|null;

    constructor(localId: number, annotation: Annotation, {remoteId=null, state=<CommentState>'default', author='', text='', replies=[], newReply=''}) {
        this.localId = localId;
        this.annotation = annotation;
        this.remoteId = remoteId;
        this.state = state;
        this.author = author;
        this.text = text;
        this.replies = replies;
        this.newReply = newReply;

        this._element = null;
    }

    static makeNew(localId: number, annotation: Annotation): Comment {
        return new Comment(localId, annotation, {state: 'creating'});
    }

    static fromApi(localId: number, annotation: Annotation, data: any): Comment {
        return new Comment(localId, annotation, {remoteId: data.id, author: data.author, text: data.text});
    }

    clone() {
        return new Comment(this.localId, this.annotation, {
            remoteId: this.remoteId,
            state: this.state,
            author: this.author,
            text: this.text,
            replies: this.replies,
            newReply: this.newReply,
        });
    }

    getDesiredPosition(): number {
        if (this.annotation.highlights.length > 0) {
            return this.annotation.highlights[0].getBoundingClientRect().top + window.scrollY;
        }
    }

    getElement(containerElement: HTMLElement): HTMLElement {
        if (!this._element) {
            this._element = document.querySelector(`[data-comment-id="${this.localId}"]`);
        }

        return this._element;
    }

    getDateDisplay() {
        return "FOO";
    }

    async delete(api: APIClient) {
        this.state = 'deleting';

        if (this.remoteId) {
            await fetch(`${api.baseUrl}/comments/${this.remoteId}/`, {
                method: 'DELETE',
                headers: {
                    'X-Review-Token': api.reviewToken,
                },
            });
        }

        this.annotation.onDelete();
        this.state = 'deleted';
    }

    async save(api: APIClient) {
        this.state = 'saving';

        // TODO: PUT if has remote id

        let response = await fetch(`${api.baseUrl}/comments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Review-Token': api.reviewToken,
            },
            body: JSON.stringify({
                'quote': this.annotation.annotation.quote,
                'text': this.text,
                'is_resolved': false,
                'content_path': this.annotation.contentPath,
                'start_xpath': this.annotation.annotation.ranges[0].start || '.',
                'start_offset': this.annotation.annotation.ranges[0].startOffset,
                'end_xpath': this.annotation.annotation.ranges[0].end || '.',
                'end_offset': this.annotation.annotation.ranges[0].endOffset,
            }),
        });

        let commentData = await response.json();

        this.state = 'default';
        this.remoteId = commentData.id;

        // TODO: Set other attributes from response
    }
}
