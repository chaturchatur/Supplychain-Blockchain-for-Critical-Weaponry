// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.4.22 <0.9.0;

contract Part{

    modifier onlyBy{
        require(current_handler == msg.sender,"This part is restricted to the current handler only");
        _;
    }

    string public entity_id;
    string public part_id;
    string public current_status;
    string public current_loc;
    address public current_handler;
    address public transferee;
    address public indent;
    string public maintenance_status;
    mapping (string=>bool) maintenance_types;

    constructor(string memory _entity_id ,string memory _part_id,string memory _current_status,string memory _current_loc,address _current_handler,string memory _maintenance_status){
        entity_id = _entity_id;
        part_id = _part_id;
        current_status = _current_status;
        current_loc = _current_loc;
        current_handler = _current_handler;
        indent = msg.sender;
        maintenance_types['A'] = true;
        maintenance_types['B'] = true;
        maintenance_types['C'] = true;
        maintenance_types['D'] = true;
        maintenance_types['E'] = true;
        maintenance_types['F'] = true;
        require(maintenance_types[_maintenance_status],"Invalid maintenance type");
        maintenance_status = _maintenance_status;
    }

    event OwnershipTransfer();

    function request_ownership() public{
        transferee = msg.sender;
    }

    function change_handler() public onlyBy(){
        current_handler = transferee;
        transferee = address(0);
        emit OwnershipTransfer();
    } 

    function change_status(string memory _current_status) public onlyBy(){
        current_status = _current_status;
    }

    function change_loc(string memory _current_loc) public onlyBy(){
        current_loc = _current_loc;
    }

    function change_maintenance(string memory _current_maintenance) public onlyBy(){
        require(maintenance_types[_current_maintenance],"Invalid maintenance type");
        maintenance_status = _current_maintenance;
    }

}