use scrypto::prelude::*;


#[derive(NonFungibleData)]
struct NftData {
    first_name : String,
    last_name : String,
    ban_reason : String,
    birthday : String
}

blueprint! {
    struct DoNotFly {
        // Vault that will store the minted NFTs
        no_fly: Vault,
        // Resource definition of the NFT
        no_fly_def: ResourceAddress,
        // Vault to contain the collected XRD
        collected_xrd: Vault,
        // Resource definition of the admin badge, able to call the `mint_nft` method
        admin_badge: ResourceAddress,
        // Vault containing the badge allowing this component to mint
        // new NFT resources
        minting_authority: Vault,
        // Keep track of the number of NFT minted
        nb_nft_minted: u64
    }

    impl DoNotFly {
        pub fn instantiate_list() -> (ComponentAddress, Bucket) {
            // Create an admin badge that will be returned to the caller
            let admin_badge: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "admin badge")
                .initial_supply(1);

            // Create a minting authority badge, that will be kept
            // inside the component to be able to mint NFTs later
            let minting_authority: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "minter authority")
                .metadata("description", "Badge that has the authority to mint new NFTs")
                .initial_supply(1);

            // Create the resource definition of the NFTs.
            // We specify that the `minting_authority` badge, created in the previous step
            // will be able to mint this resource.
            let nofly_address: ResourceAddress = ResourceBuilder::new_non_fungible()
                .metadata("name", "Do Not Fly NFT")
                .mintable(rule!(require(minting_authority.resource_address())), LOCKED)
                .no_initial_supply();

            // Only someone presenting the admin_badge will be able to call
            // the "mint_nft" method.
            let access_rules = AccessRules::new()
                .method("mint_nft", rule!(require(admin_badge.resource_address())))
                .default(rule!(allow_all));
            
            // Instantiate the component
            let mut component = Self {
                no_fly: Vault::new(nofly_address),
                no_fly_def: nofly_address,
                collected_xrd: Vault::new(RADIX_TOKEN),
                admin_badge: admin_badge.resource_address(),
                minting_authority: Vault::with_bucket(minting_authority),
                nb_nft_minted: 0
            }
            .instantiate();
            component.add_access_check(access_rules);

            (component.globalize(), admin_badge)
        }

        // Admins can call this method to mint new nft
        // NFTs with specific attributes
        pub fn mint_nft(&mut self, first_name: String, last_name: String, ban_reason: String, birthday: String) {
            // The id of the minted NFT will be an increasing number, starting with 1
            let nft_id = NonFungibleId::from_u64(self.nb_nft_minted + 1);

            // Initiate the data that the NFT will hold
            let nft_data: NftData = NftData{
                first_name,
                last_name,
                ban_reason,
                birthday
            };

            // Mint a new NFT
            let new_nft = self.minting_authority.authorize(|| {
                return borrow_resource_manager!(self.no_fly_def).mint_non_fungible(
                    &nft_id,
                    nft_data,
                );
            });

            // Insert the newly minted NFT in the component's vault
            self.no_fly.put(new_nft);
            self.nb_nft_minted += 1;
        }

    }
}
