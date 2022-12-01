# Do Not Fly List NFT
Creating NFTs

## How to run
1. save the XRD resource address: 
    ```bash
    // On Linux and Mac
    export xrd=resource_sim1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzqu57yag
    // On Windows Powershell
    $xrd="resource_sim1qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzqu57yag"
    ```
2. Reset your environment: `resim reset`
3. Create a new account: `resim new-account` -> save into **$account**
4. Build and deploy the blueprint on the local ledger: `resim publish .` -> save into **$package**
5. Call the `instantiate_club` function to instantiate a component: `resim call-function $package DoNotFly instantiate_list` -> save into **$component** and **$admin_badge**