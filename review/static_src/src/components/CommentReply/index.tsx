import * as React from 'react';
import { CommentReply } from '../../state';
import APIClient from '../../api';

import './style.scss';

export interface CommentReplyProps {
    reply: CommentReply;
    store: any;
    api: APIClient;
}

export default class CommentReplyComponent extends React.Component<CommentReplyProps> {
    render() {
        let { reply } = this.props;

        let onClickEdit = e => {

        };

        let onClickDelete = e => {

        };

        return (
            <li className="comment-reply">
                <p className="comment-reply__text">{reply.text}</p>
                <div className="comment-reply__actions">
                    <a href="#" onClick={onClickEdit}>Edit</a>
                    <a href="#" onClick={onClickDelete}>Delete</a>
                </div>
            </li>
        );
    }
}
