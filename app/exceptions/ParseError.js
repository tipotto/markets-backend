/* eslint-disable node/no-unsupported-features */
class ParseError extends Error {
  constructor(errorMessage) {
    super(errorMessage);
    this.name = new.target.name;
    Object.setPrototypeOf(this, new.target.prototype);
  }
}

export default ParseError;
