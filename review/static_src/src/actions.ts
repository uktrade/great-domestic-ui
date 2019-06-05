import {Comment, CommentUpdate} from './state';

export const ADD_COMMENT = 'add-comment';
export const UPDATE_COMMENT = 'update-comment';
export const DELETE_COMMENT = 'delete-comment';

export interface AddCommentAction {
    type: 'add-comment',
    comment: Comment
}

export interface UpdateCommentAction {
    type: 'update-comment',
    commentId: number,
    update: CommentUpdate
}

export interface DeleteCommentAction {
    type: 'delete-comment',
    commentId: number,
}

export type Action = AddCommentAction | UpdateCommentAction | DeleteCommentAction;

export function addComment(comment: Comment): AddCommentAction {
    return {
        type: ADD_COMMENT,
        comment,
    };
}

export function updateComment(commentId: number, update: CommentUpdate): UpdateCommentAction {
    return {
        type: UPDATE_COMMENT,
        commentId,
        update,
    };
}

export function deleteComment(commentId: number): DeleteCommentAction {
    return {
        type: DELETE_COMMENT,
        commentId,
    };
}
