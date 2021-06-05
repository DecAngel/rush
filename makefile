train_xian:
	python -m models.MNAD.Train_xian

eval_mnad:
	 python -m  models.MNAD.Evaluate --model_dir models/MNAD/exp/ShanghaiTech/pred/log/model.pth --m_items_dir models/MNAD/exp/ShanghaiTech/pred/log/keys.pt

server:
	python -m flask_server

main:
	python -m framework.main