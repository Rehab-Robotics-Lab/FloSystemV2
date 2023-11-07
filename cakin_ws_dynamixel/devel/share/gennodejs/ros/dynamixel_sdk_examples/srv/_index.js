
"use strict";

let GetPosition = require('./GetPosition.js')
let SyncGetPosition = require('./SyncGetPosition.js')
let BulkGetItem = require('./BulkGetItem.js')

module.exports = {
  GetPosition: GetPosition,
  SyncGetPosition: SyncGetPosition,
  BulkGetItem: BulkGetItem,
};
