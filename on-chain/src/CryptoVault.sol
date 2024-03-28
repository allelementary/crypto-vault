// SPDX-License-Identifier: MIT

pragma solidity ^0.8.22;

/*
 * @title CryptoVault
 * @author Mikhail Antonov
 *
 * Store encrypted data on-chain. Data is stored under user's address, app name and environment name
 */
contract CryptoVault {
    mapping(address => mapping(bytes => mapping(bytes => bytes))) private UserToSecret;

    /* @dev store encrypted data on-chain
    * Data is stored under user's address, app name and environment name
    * @param data: encrypted data, bytes
    */
    function store(bytes memory app, bytes memory env, bytes memory data) external {
        UserToSecret[msg.sender][app][env] = data;
    }

    /* @dev retrieve encrypted data
    * Despite all on-chain data is visible for anyone, function should return only msg.sender data
    * Stored data should be encrypted off-chain first
    */
    function retrieve(bytes memory app, bytes memory env) external view returns (bytes memory) {
        return UserToSecret[msg.sender][app][env];
    }
}
