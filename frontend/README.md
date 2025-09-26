

## 起動方法

### Dockerを用いた起動方法(推奨)

#### Development Mode
```bash
make up
```

#### Production Mode
```bash
# プロダクションビルド
make prod-build

# プロダクションサーバーを起動
make start
```

#### Other Commands
```bash
# サービスを停止
make down

# サービスの状態を確認
make status
```

### ローカルでの起動方法

```bash
    pnpm run dev
```



