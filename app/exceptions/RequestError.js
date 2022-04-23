/* eslint-disable node/no-unsupported-features */
class RequestError extends Error {
  constructor(errorMessage) {
    super(errorMessage);
    this.name = new.target.name;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

export default RequestError;
