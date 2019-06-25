import { APIClient, initCommentsApp } from 'wagtail-review-ui';

declare var window: any;

window['CommentsAPI'] = APIClient;
window['initCommentsApp'] = initCommentsApp;
