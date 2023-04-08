import glob
import tweepy
import time
import random
from PIL import Image, ImageDraw, ImageFont
import textwrap


api_key = ''
api_secret_key = ''
bearer_token = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

caminho = '/home/kiwiyo/anibot/'
imagens = glob.glob(caminho + '/*.jpeg')

def cria_meme(imagem, texto):
    with Image.open(imagem).convert("RGBA") as base:

		# cria uma imagem em branco para o texto e com transparencia total
	    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

	    # tamanho font
	    tamanho = round(base.size[0] * 0.08)

	    # seleciona a fonte
	    fnt = ImageFont.truetype("/home/kiwiyo/anibot/impact.ttf", tamanho)

	    # cria o objeto desenho
	    d = ImageDraw.Draw(txt)

	    # justifica o texto
	    wraped_text = textwrap.wrap(texto, width=35)
	    text = '\n'.join(wraped_text)

	    # verifica o tamanho do texto para centralização
	    text_size = d.textsize(text, font=fnt)

	    # define x e y para parametros de definição do local do texto
	    x = (base.size[0] - text_size[0]) / 2
	    y = (base.size[1] - text_size[1]) / 1.2

	    # inclui o texto na imagem em branco
	    d.multiline_text((x, y), text, font=fnt, fill=(255,255,0), stroke_width=5, stroke_fill=(0,0,0), align='center')

	    # junta o texto com a imagem
	    out = Image.alpha_composite(base, txt)

	    caminho_salvar = '/home/kiwiyo/anibot/imagem_twt.png'

	    out.convert("RGB").save(caminho_salvar)

	    return caminho_salvar


nm_arquivo = '/home/kiwiyo/anibot/ultimo_id.txt'

def recuperar_ultimo_id(nm_arquivo):
	f_read = open(nm_arquivo, 'r')
	ultimo_id = int(f_read.read().strip())
	f_read.close()
	return ultimo_id

def guardar_ultimo_id(ultimo_id, nm_arquivo):
	f_write = open(nm_arquivo, 'w')
	f_write.write(str(ultimo_id))
	f_write.close()
	return


def respondendo_tweets():
	print('recuperando e respondendo tweets...', flush = True)

	ultimo_id = recuperar_ultimo_id(nm_arquivo)

	mentions = api.mentions_timeline(ultimo_id, tweet_mode = 'extended')

	for mention in reversed(mentions):
		print(str(mention.id) + ' - ' + mention.full_text, flush = True)
		ultimo_id = mention.id
		guardar_ultimo_id(ultimo_id, nm_arquivo)

		print('menção encontrada', flush=True)
		print('mandando meme...', flush=True)

		texto = mention.full_text
		texto = re.sub(r'@\w+', '', texto)

		status = '@' + mention.user.screen_name

		meme = cria_meme(random.choice(imagens), texto)

		imagem_upload = api.media_upload(meme)

		imagem_id = [imagem_upload.media_id_string]

		api.update_status(in_reply_to_status_id = ultimo_id, media_ids = imagem_id, status = status)


while True:
	respondendo_tweets()
	time.sleep(15)
