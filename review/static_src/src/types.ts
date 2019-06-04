import APIClient from './api';
import {Annotation} from './annotation';

export class CommentReply {
    text: string;

    constructor(text: string) {
        this.text = text;
    }
}

class BaseComment {
    id: number;
    annotation: Annotation;
    _element: HTMLElement|null;

    constructor(id: number, annotation: Annotation) {
        this.id = id;
        this.annotation = annotation;

        this._element = null;
    }

    getDesiredPosition(): number {
        if (this.annotation.highlights.length > 0) {
            return this.annotation.highlights[0].getBoundingClientRect().top + window.scrollY;
        }
    }

    getElement(containerElement: HTMLElement): HTMLElement {
        if (!this._element) {
            this._element = document.querySelector(`[data-comment-id="${this.id}"]`);
        }

        return this._element;
    }
}

export class Comment extends BaseComment {
    remoteId: number;
    author: string;
    text: string;
    isDeleting: boolean;
    replies: CommentReply[];
    replyInProgress: string;

    constructor(id: number, data: any, annotation: Annotation) {
        super(id, annotation);

        this.remoteId = data.id;
        this.author = "AUTHOR";
        this.text = data.text;
        this.isDeleting = false;
        this.replies = [];
        this.replyInProgress = '';
    }

    getDateDisplay() {
        return "DATE";
    }

    async delete(api: APIClient) {
        this.isDeleting = true;

        await fetch(`${api.baseUrl}/comments/${this.remoteId}/`, {
            method: 'DELETE',
            headers: {
                'X-Review-Token': api.reviewToken,
            },
        });

        this.annotation.onDelete();
    }
}

export class NewComment extends BaseComment {
    text: string;
    isNew: boolean;
    isSubmitting: boolean;

    constructor(id: number, annotation: Annotation) {
        super(id, annotation);
        this.text = "";
        this.isNew = true;
        this.isSubmitting = false;
    }

    async submit(api: APIClient) {
        this.isSubmitting = true;

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

        return new Comment(this.id, await response.json(), this.annotation);
    }

    cancel() {
        this.annotation.onDelete();
    }
}
