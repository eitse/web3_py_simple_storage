// SPDX-License-Identifier: MIT
pragma solidity 0.8.2;

contract SimpleStorage {
    uint256 favouriteNumber;
    bool favouriteBool;

    struct People {
        uint256 favouriteNumber;
        string name;
    }

    People[] public people;

    mapping(string => uint256) public NameToFavouriteNo;

    function store(uint256 _favouriteNumber) public {
        favouriteNumber = _favouriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favouriteNumber;
    }

    function addPerson(uint256 _favouriteNumber, string memory _name) public {
        people.push(People(_favouriteNumber, _name));
        NameToFavouriteNo[_name] = _favouriteNumber;
    }
}
