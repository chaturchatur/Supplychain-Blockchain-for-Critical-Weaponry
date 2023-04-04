// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.16 <0.9.0;

import './Part.sol';

contract Indent{
    address public owner;
    address public creator;
    address public transferee;
    bool public restricted;
    uint public creation_date;
    address public reviser;
    uint public modify_date;
    uint public fill_date;
   
    struct part_order{
        // Part uuid
        string part_id;
        uint dues_out;
        uint dues_in;
        address [] parts;
    } 

    mapping(string=>uint) part_order_mapping;
    part_order [] public part_orders;

    modifier onlyBy {
        if (restricted){
            require(msg.sender == owner,"This indent is restricted to owner");
        }
        _;
    }
    event OwnershipTransfer();

    function request_ownership() public{
        transferee = msg.sender;
    }

    function change_handler() public onlyBy(){
        owner = transferee;
        transferee = address(0);
        emit OwnershipTransfer();
    }

    constructor(bool _restricted) {
        owner = msg.sender;
        creator = msg.sender;
        creation_date = block.timestamp;
        modify_date = block.timestamp;
        restricted = _restricted;
    }

    function add_edit_order(string memory _part_id,uint _dues_out,uint _dues_in) public onlyBy returns(uint order_id){
        reviser = msg.sender;
        modify_date = block.timestamp;
        address [] memory part_list;
        uint pos = part_order_mapping[_part_id];
        if ( pos != 0){
            part_order memory order = part_orders[pos - 1];
            order.dues_in = _dues_in;
            order.dues_out = _dues_out;
            order_id = part_orders.length;
        }
        else {
            part_order memory order = part_order(_part_id,_dues_out,_dues_in,part_list);
            part_orders.push(order);
            order_id = part_orders.length;
            part_order_mapping[_part_id] = order_id;
        }
    }

    function get_part_orders() external view returns(part_order [] memory orders){
        orders = part_orders;
    }

    function get_registered_part_list(string memory _part_id) external view returns(address [] memory parts){
        uint pos = part_order_mapping[_part_id];
        require(pos > 0,'Part order does not exist');
        part_order memory order = part_orders[pos - 1];
        parts = order.parts;
    }

    function register_part(string memory _entity_id ,string memory _part_id,string memory _current_status,string memory _current_loc,string memory _maintenance_status) public onlyBy returns(address entity_address){
        Part entity = new Part(_entity_id,_part_id,_current_status,_current_loc,msg.sender,_maintenance_status);
        uint pos = part_order_mapping[_part_id];
        require(pos > 0,'Part order does not exist');
        part_order storage order = part_orders[pos - 1];
        entity_address = address(entity);
        order.parts.push(entity_address);
        order.dues_in++;
    }
}