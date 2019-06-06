import {Annotation} from './utils/annotation';
import * as actions from './actions';

export class Author {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    static unknown(): Author {
        return new Author("Unknown");
    }

    static fromApi(data: any): Author {
        return new Author(data.name);
    }
}

export type CommentReplyMode = 'default' | 'editing' | 'saving' | 'deleting' | 'deleted' | 'save_error' | 'delete_error';

export class CommentReply {
    localId: number;
    remoteId: number|null;
    mode: CommentReplyMode;
    author: string;
    text: string;
    editPreviousText: string;

    constructor(localId, {remoteId=null, mode=<CommentReplyMode>'default', author='', text='', replies=[], newReply=''}) {
        this.localId = localId;
        this.remoteId = remoteId;
        this.mode = mode;
        this.author = author;
        this.text = text;
        this.editPreviousText = '';
    }

    static fromApi(localId: number, data: any): CommentReply {
        return new CommentReply(localId, {remoteId: data.id, author: data.author, text: data.text});
    }
}

export interface CommentReplyUpdate {
    remoteId?: number|null;
    mode?: CommentReplyMode;
    author?: Author;
    text?: string;
    editPreviousText?: string;
}

export type CommentMode = 'default' | 'creating' | 'editing' | 'saving' | 'deleting' | 'deleted' | 'save_error' | 'delete_error';

export class Comment {
    localId: number;
    annotation: Annotation;
    remoteId: number|null;
    mode: CommentMode;
    author: Author;
    text: string;
    replies: {[replyId: number]: CommentReply};
    newReply: string;
    editPreviousText: string;

    constructor(localId: number, annotation: Annotation, {remoteId=null, mode=<CommentMode>'default', author=Author.unknown(), text='', replies={}, newReply=''}) {
        this.localId = localId;
        this.annotation = annotation;
        this.remoteId = remoteId;
        this.mode = mode;
        this.author = author;
        this.text = text;
        this.replies = replies;
        this.newReply = newReply;
        this.editPreviousText = '';
    }

    static makeNew(localId: number, annotation: Annotation): Comment {
        return new Comment(localId, annotation, {mode: 'creating'});
    }

    static fromApi(localId: number, annotation: Annotation, data: any): Comment {
        return new Comment(localId, annotation, {remoteId: data.id, author: data.author, text: data.text});
    }
}

export interface CommentUpdate {
    annotation?: Annotation;
    remoteId?: number|null;
    mode?: CommentMode;
    author?: Author;
    text?: string;
    newReply?: string;
    editPreviousText?: string;
}

interface State {
    comments: {[commentId: number]: Comment},
}

function initialState(): State {
    return {
        comments: {}
    };
}

export function reducer(state: State|undefined, action: actions.Action) {
    if (typeof state === 'undefined') {
        state = initialState();
    }

    switch (action.type) {
        case actions.ADD_COMMENT:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            state.comments[action.comment.localId] = action.comment;
            break;

        case actions.UPDATE_COMMENT:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            state.comments[action.commentId] = Object.assign({}, state.comments[action.commentId], action.update);
            break;

        case actions.DELETE_COMMENT:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            delete state.comments[action.commentId]
            break;

        case actions.ADD_REPLY:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            state.comments[action.commentId] = Object.assign({}, state.comments[action.commentId], {
                replies: Object.assign({}, state.comments[action.commentId].replies),
            });
            state.comments[action.commentId].replies[action.reply.localId] = action.reply;
            break;

        case actions.UPDATE_REPLY:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            state.comments[action.commentId] = Object.assign({}, state.comments[action.commentId], {
                replies: Object.assign({}, state.comments[action.commentId].replies),
            });
            state.comments[action.commentId].replies[action.replyId] = Object.assign({}, state.comments[action.commentId].replies[action.replyId], action.update);
            break;

        case actions.DELETE_REPLY:
            state = Object.assign({}, state, {
                comments: Object.assign({}, state.comments),
            });
            state.comments[action.commentId] = Object.assign({}, state.comments[action.commentId], {
                replies: Object.assign({}, state.comments[action.commentId].replies),
            });
            delete state.comments[action.commentId].replies[action.replyId]
            break;

    }

    console.log(state, action);

    return state;
}
