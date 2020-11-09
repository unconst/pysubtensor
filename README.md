
## Run

```bash
cd subtensor
cargo build --release
./target/release/node-subtensor purge-chain --dev
./target/release/node-subtensor --dev

cd ..
python test.py
```
