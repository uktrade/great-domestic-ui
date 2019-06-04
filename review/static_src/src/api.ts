export default class APIClient {
    baseUrl: string;
    reviewToken: string;

    constructor(baseUrl: string, reviewToken: string) {
        this.baseUrl = baseUrl;
        this.reviewToken = reviewToken;
    }
}
