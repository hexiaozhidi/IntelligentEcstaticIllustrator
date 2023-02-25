default_prompt = 'amazing,(((beautiful detailed eyes))), (1girl), finely detail, depth of field, extremely detailed ' \
                 'CG unity 8k wallpaper, (best quality), ((masterpiece)), (highres), original, extremely detailed ' \
                 'wallpaper, (an extremely delicate and beautiful)'

default_negative_prompt = 'nsfw, multiple breasts, (mutated hands and fingers:1.5 ), (long body :1.3), (mutation, ' \
                          'poorly drawn :1.2) , black-white, bad anatomy, liquid body, liquid tongue, disfigured, ' \
                          'malformed, mutated, anatomical nonsense, text font ui, error, malformed hands, long neck, ' \
                          'blurred, lowers, lowres, bad anatomy, bad proportions, bad shadow, uncoordinated body, ' \
                          'unnatural body, fused breasts, bad breasts, huge breasts, poorly drawn breasts, ' \
                          'extra breasts, liquid breasts, heavy breasts, missing breasts, huge haunch, huge thighs, ' \
                          'huge calf, bad hands, fused hand, missing hand, disappearing arms, disappearing thigh, ' \
                          'disappearing calf, disappearing legs, fused ears, bad ears, poorly drawn ears, extra ears, ' \
                          'liquid ears, heavy ears, missing ears, fused animal ears, bad animal ears, poorly drawn ' \
                          'animal ears, extra animal ears, liquid animal ears, heavy animal ears, missing animal ' \
                          'ears, text, ui, error, missing fingers, missing limb, fused fingers, one hand with more ' \
                          'than 5 fingers, one hand with less than 5 fingers, one hand with more than 5 digit, ' \
                          'one hand with less than 5 digit, extra digit, fewer digits, fused digit, missing digit, ' \
                          'bad digit, liquid digit, colorful tongue, black tongue, cropped, watermark, username, ' \
                          'blurry, JPEG artifacts, signature, 3D, 3D game, 3D game scene, 3D character, ' \
                          'malformed feet, extra feet, bad feet, poorly drawn feet, fused feet, missing feet, ' \
                          'extra shoes, bad shoes, fused shoes, more than two shoes, poorly drawn shoes, bad gloves, ' \
                          'poorly drawn gloves, fused gloves, bad cum, poorly drawn cum, fused cum, bad hairs, ' \
                          'poorly drawn hairs, fused hairs, big muscles, ugly, bad face, fused face, poorly drawn ' \
                          'face, cloned face, big face, long face, bad eyes, fused eyes poorly drawn eyes, ' \
                          'extra eyes, malformed limbs, more than 2 nipples, missing nipples, different nipples, ' \
                          'fused nipples, bad nipples, poorly drawn nipples, black nipples, colorful nipples, ' \
                          'gross proportions. short arm, (((missing arms))), missing thighs, missing calf, ' \
                          'missing legs, mutation, duplicate, morbid, mutilated, poorly drawn hands, more than 1 left ' \
                          'hand, more than 1 right hand, deformed, (blurry), disfigured, missing legs, extra arms, ' \
                          'extra thighs, more than 2 thighs, extra calf, fused calf, extra legs, bad knee, ' \
                          'extra knee, more than 2 legs, bad tails, bad mouth, fused mouth, poorly drawn mouth, ' \
                          'bad tongue, tongue within mouth, too long tongue, black tongue, big mouth, cracked mouth, ' \
                          'bad mouth, dirty face, dirty teeth, dirty pantie, fused pantie, poorly drawn pantie, ' \
                          'fused cloth, poorly drawn cloth, bad pantie, yellow teeth, thick lips, bad cameltoe, ' \
                          'colorful cameltoe, bad asshole, poorly drawn asshole, fused asshole, missing asshole, ' \
                          'bad anus, bad pussy, bad crotch, bad crotch seam, fused anus, fused pussy, fused anus, ' \
                          'fused crotch, poorly drawn crotch, fused seam, poorly drawn anus, poorly drawn pussy, ' \
                          'poorly drawn crotch, poorly drawn crotch seam, bad thigh gap, missing thigh gap, ' \
                          'fused thigh gap, liquid thigh gap, poorly drawn thigh gap, poorly drawn anus, ' \
                          'bad collarbone, fused collarbone, missing collarbone, liquid collarbone, strong girl, ' \
                          'obesity, worst quality, low quality, normal quality, liquid tentacles, bad tentacles, ' \
                          'poorly drawn tentacles, split tentacles, fused tentacles, missing clit, bad clit, ' \
                          'fused clit, colorful clit, black clit, liquid clit, QR code, bar code, censored, ' \
                          'safety panties, safety knickers, beard, furry ,pony, pubic hair, mosaic, excrement, ' \
                          'faeces, shit, futa, testis'


class Payload:
    def __init__(
            self,
            prompt: str = '',
            negative_prompt: str = '',
            steps: int = 20,  # API default value: 50
            sampler_name: str = 'Euler a',  # API default value: "Euler"
            width: int = 512,
            height: int = 512,
            restore_faces: bool = False,
            tiling: bool = False,
            enable_hr: bool = False,
            firstphase_width: int = 0,
            firstphase_height: int = 0,
            denoising_strength: float = 0.7,  # API default value: 0
            n_iter: int = 1,
            batch_size: int = 1,
            cfg_scale: float = 7.0,
            seed: int = -1,
            subseed: int = -1,
            subseed_strength: float = 0.0,
            seed_resize_from_w: int = 0,  # API default value: -1
            seed_resize_from_h: int = 0,  # API default value: -1
            eta: float = 0.0,
            s_churn: float = 0.0,
            s_tmin: float = 0.0,
            s_noise: float = 1.0
    ):
        self.prompt: str = prompt + ', ' + default_prompt  # Prompt
        self.negative_prompt: str = negative_prompt + ', ' + default_negative_prompt  # Negative prompt

        self.steps: int = steps  # Sampling Steps
        self.sampler_name: str = sampler_name  # Sampling method

        self.width: int = width  # Width
        self.height: int = height  # Height

        self.restore_faces: bool = restore_faces  # Restore faces
        self.tiling: bool = tiling  # Tiling

        self.enable_hr: bool = enable_hr  # Highres. fix
        self.firstphase_width: int = firstphase_width  # Firstpass width
        self.firstphase_height: int = firstphase_height  # Firstpass height
        self.denoising_strength: float = denoising_strength  # Denoising strength

        self.n_iter: int = n_iter  # Batch count
        self.batch_size: int = batch_size  # Batch size

        self.cfg_scale: float = cfg_scale  # CFG Scale

        self.seed: int = seed  # Seed

        self.subseed: int = subseed  # Variation seed
        self.subseed_strength: float = subseed_strength  # Variation strength
        self.seed_resize_from_w: int = seed_resize_from_w  # Resize seed from width
        self.seed_resize_from_h: int = seed_resize_from_h  # Resize seed from height

        self.eta: float = eta  # eta (noise multiplier) for DDIM
        self.s_churn: float = s_churn  # sigma churn
        self.s_tmin: float = s_tmin  # sigma tmin
        self.s_noise: float = s_noise  # sigma noise

    def __str__(self):
        short_prompt = f'{self.prompt[:10]}{"..." if len(self.prompt) > 10 else ""}'
        steps = f'{self.steps} step{"s" if self.steps > 1 else ""}'
        return f'Payload "{short_prompt}" with {steps}'
