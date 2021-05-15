eval_mnad:
	 python -m  models.MNAD.Evaluate --model_dir models/MNAD/exp/ShanghaiTech/pred/log/model.pth --m_items_dir models/MNAD/exp/ShanghaiTech/pred/log/keys.pt

main:
	python -m framework.main