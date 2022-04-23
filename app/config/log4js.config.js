/* eslint-disable node/no-unsupported-features */
import log4js from 'log4js';

log4js.configure('./app/config/log4js.config.json');
export const system = log4js.getLogger('system');
export const http = log4js.getLogger('http');
export const access = log4js.getLogger('access');
