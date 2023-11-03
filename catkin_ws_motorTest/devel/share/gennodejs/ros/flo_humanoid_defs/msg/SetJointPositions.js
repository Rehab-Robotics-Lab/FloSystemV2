// Auto-generated. Do not edit!

// (in-package flo_humanoid_defs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class SetJointPositions {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.id1 = null;
      this.id2 = null;
      this.id3 = null;
      this.id4 = null;
      this.item1 = null;
      this.item2 = null;
      this.item3 = null;
      this.item4 = null;
      this.value1 = null;
      this.value2 = null;
      this.value3 = null;
      this.value4 = null;
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
      if (initObj.hasOwnProperty('id3')) {
        this.id3 = initObj.id3
      }
      else {
        this.id3 = 0;
      }
      if (initObj.hasOwnProperty('id4')) {
        this.id4 = initObj.id4
      }
      else {
        this.id4 = 0;
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
      if (initObj.hasOwnProperty('item3')) {
        this.item3 = initObj.item3
      }
      else {
        this.item3 = '';
      }
      if (initObj.hasOwnProperty('item4')) {
        this.item4 = initObj.item4
      }
      else {
        this.item4 = '';
      }
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
      if (initObj.hasOwnProperty('value3')) {
        this.value3 = initObj.value3
      }
      else {
        this.value3 = 0;
      }
      if (initObj.hasOwnProperty('value4')) {
        this.value4 = initObj.value4
      }
      else {
        this.value4 = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type SetJointPositions
    // Serialize message field [id1]
    bufferOffset = _serializer.uint8(obj.id1, buffer, bufferOffset);
    // Serialize message field [id2]
    bufferOffset = _serializer.uint8(obj.id2, buffer, bufferOffset);
    // Serialize message field [id3]
    bufferOffset = _serializer.uint8(obj.id3, buffer, bufferOffset);
    // Serialize message field [id4]
    bufferOffset = _serializer.uint8(obj.id4, buffer, bufferOffset);
    // Serialize message field [item1]
    bufferOffset = _serializer.string(obj.item1, buffer, bufferOffset);
    // Serialize message field [item2]
    bufferOffset = _serializer.string(obj.item2, buffer, bufferOffset);
    // Serialize message field [item3]
    bufferOffset = _serializer.string(obj.item3, buffer, bufferOffset);
    // Serialize message field [item4]
    bufferOffset = _serializer.string(obj.item4, buffer, bufferOffset);
    // Serialize message field [value1]
    bufferOffset = _serializer.int32(obj.value1, buffer, bufferOffset);
    // Serialize message field [value2]
    bufferOffset = _serializer.int32(obj.value2, buffer, bufferOffset);
    // Serialize message field [value3]
    bufferOffset = _serializer.int32(obj.value3, buffer, bufferOffset);
    // Serialize message field [value4]
    bufferOffset = _serializer.int32(obj.value4, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type SetJointPositions
    let len;
    let data = new SetJointPositions(null);
    // Deserialize message field [id1]
    data.id1 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [id2]
    data.id2 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [id3]
    data.id3 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [id4]
    data.id4 = _deserializer.uint8(buffer, bufferOffset);
    // Deserialize message field [item1]
    data.item1 = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [item2]
    data.item2 = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [item3]
    data.item3 = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [item4]
    data.item4 = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [value1]
    data.value1 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [value2]
    data.value2 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [value3]
    data.value3 = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [value4]
    data.value4 = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += _getByteLength(object.item1);
    length += _getByteLength(object.item2);
    length += _getByteLength(object.item3);
    length += _getByteLength(object.item4);
    return length + 36;
  }

  static datatype() {
    // Returns string type for a message object
    return 'flo_humanoid_defs/SetJointPositions';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '009ce4d7a30096c5b116ae7327067969';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    #Message definition to set the position of all the joints of 1 arm in the humanoid robot
    #(4 joints in each arm, 2 at the shoulder and 2 at the elbow) 
    uint8 id1
    uint8 id2
    uint8 id3
    uint8 id4
    string item1
    string item2
    string item3
    string item4
    int32 value1
    int32 value2
    int32 value3
    int32 value4
    
    
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new SetJointPositions(null);
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

    if (msg.id3 !== undefined) {
      resolved.id3 = msg.id3;
    }
    else {
      resolved.id3 = 0
    }

    if (msg.id4 !== undefined) {
      resolved.id4 = msg.id4;
    }
    else {
      resolved.id4 = 0
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

    if (msg.item3 !== undefined) {
      resolved.item3 = msg.item3;
    }
    else {
      resolved.item3 = ''
    }

    if (msg.item4 !== undefined) {
      resolved.item4 = msg.item4;
    }
    else {
      resolved.item4 = ''
    }

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

    if (msg.value3 !== undefined) {
      resolved.value3 = msg.value3;
    }
    else {
      resolved.value3 = 0
    }

    if (msg.value4 !== undefined) {
      resolved.value4 = msg.value4;
    }
    else {
      resolved.value4 = 0
    }

    return resolved;
    }
};

module.exports = SetJointPositions;
