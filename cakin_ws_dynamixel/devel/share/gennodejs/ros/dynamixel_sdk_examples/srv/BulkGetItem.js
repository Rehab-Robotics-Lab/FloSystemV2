// Auto-generated. Do not edit!

// (in-package dynamixel_sdk_examples.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class BulkGetItemRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.id1 = null;
      this.id2 = null;
      this.item1 = null;
      this.item2 = null;
    }
    else {
      if (initObj.hasOwnProperty('id1')) {
        this.id1 = initObj.id1
      }
      else {
        this.id1 = 0;
      }
      if (initObj.hasOwnProperty('id2')) {
        this.id2 = initObj.id2
      }
      else {
        this.id2 = 0;
      }
      if (initObj.hasOwnProperty('item1')) {
        this.item1 = initObj.item1
      }
      else {
        this.item1 = '';
      }
      if (initObj.hasOwnProperty('item2')) {
        this.item2 = initObj.item2
      }
      else {
        this.item2 = '';
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BulkGetItemRequest
    // Serialize message field [id1]
    bufferOffset = _serializer.uint8(obj.id1, buffer, bufferOffset);
    // Serialize message field [id2]
    bufferOffset = _serializer.uint8(obj.id2, buffer, bufferOffset);
    // Serialize message field [item1]
    bufferOffset = _serializer.string(obj.item1, buffer, bufferOffset);
    // Serialize message field [item2]
    bufferOffset = _serializer.string(obj.item2, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BulkGetItemRequest
    let len;
    let data = new BulkGetItemRequest(null);
    // Deserialize message field [id1]
    data.id1 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [id2]
    data.id2 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [item1]
    data.item1 = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [item2]
    data.item2 = _deserializer.string(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.item1);
    length += _getByteLength(object.item2);
    return length + 10;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dynamixel_sdk_examples/BulkGetItemRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f55042aa3aa499ad4bb778a05d278e5e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    uint8 id1
    uint8 id2
    string item1
    string item2
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BulkGetItemRequest(null);
    if (msg.id1 !== undefined) {
      resolved.id1 = msg.id1;
    }
    else {
      resolved.id1 = 0
    }

    if (msg.id2 !== undefined) {
      resolved.id2 = msg.id2;
    }
    else {
      resolved.id2 = 0
    }

    if (msg.item1 !== undefined) {
      resolved.item1 = msg.item1;
    }
    else {
      resolved.item1 = ''
    }

    if (msg.item2 !== undefined) {
      resolved.item2 = msg.item2;
    }
    else {
      resolved.item2 = ''
    }

    return resolved;
    }
};

class BulkGetItemResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.value1 = null;
      this.value2 = null;
    }
    else {
      if (initObj.hasOwnProperty('value1')) {
        this.value1 = initObj.value1
      }
      else {
        this.value1 = 0;
      }
      if (initObj.hasOwnProperty('value2')) {
        this.value2 = initObj.value2
      }
      else {
        this.value2 = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type BulkGetItemResponse
    // Serialize message field [value1]
    bufferOffset = _serializer.int32(obj.value1, buffer, bufferOffset);
    // Serialize message field [value2]
    bufferOffset = _serializer.int32(obj.value2, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type BulkGetItemResponse
    let len;
    let data = new BulkGetItemResponse(null);
    // Deserialize message field [value1]
    data.value1 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [value2]
    data.value2 = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'dynamixel_sdk_examples/BulkGetItemResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e5963c91be0598b7f68fed70b98f2326';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 value1
    int32 value2
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new BulkGetItemResponse(null);
    if (msg.value1 !== undefined) {
      resolved.value1 = msg.value1;
    }
    else {
      resolved.value1 = 0
    }

    if (msg.value2 !== undefined) {
      resolved.value2 = msg.value2;
    }
    else {
      resolved.value2 = 0
    }

    return resolved;
    }
};

module.exports = {
  Request: BulkGetItemRequest,
  Response: BulkGetItemResponse,
  md5sum() { return 'f0b74b4d53178e0d0ede26a30b687544'; },
  datatype() { return 'dynamixel_sdk_examples/BulkGetItem'; }
};
