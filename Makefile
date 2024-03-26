-include .env

NETWORK_ARGS := --rpc-url http://localhost:8545 --private-key $(DEFAULT_ANVIL_KEY) --broadcast

ifeq ($(findstring --network mumbai,$(ARGS)),--network mumbai)
	NETWORK_ARGS := --rpc-url $(MUMBAI_RPC_URL) --private-key $(MUMBAI_PRIVATE_KEY) --broadcast --verify --etherscan-api-key $(POLYSCAN_API_KEY) -vvvv
endif

deploy:
	echo $(MUMBAI_RPC_URL)
	@forge script script/DeployCryptoVault.s.sol:DeployCryptoVault $(NETWORK_ARGS)
