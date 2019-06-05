import {Annotation} from './utils/annotation';
import * as actions from './actions';

export interface CommentReply {
    text: string;
}

export type CommentMode = 'default' | 'creating' | 'editing' | 'saving' | 'deleting' | 'deleted' | 'save_error' | 'delete_error';

export class Comment {
    localId: number;
    annotation: Annotation;
    remoteId: number|null;
    mode: CommentMode;
    author: string;
    text: string;
    replies: CommentReply[];
    newReply: string;

    constructor(localId: number, annotation: Annotation, {remoteId=null, mode=<CommentMode>'default', author='', text='', replies=[], newReply=''}) {
        this.localId = localId;
        this.annotation = annotation;
        this.remoteId = remoteId;
        this.mode = mode;
        this.author = author;
        this.text = text;
        this.replies = replies;
        this.newReply = newReply;
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
    author?: string;
    text?: string;
    newReply?: string;
}

interface State {
    comments: {[commentId: number]: Comment},
}

function initialState(): State {
    return {
        comments: {}
    };
}

function indexOfComment(comments: Comment[], commentId: number) {
    for (let index in comments) {
        if (comments[index].localId == commentId) {
            return index;
        }
    }
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
    }

    console.log(state, action);

    return state;
}
