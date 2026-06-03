/* ============================
   VNU Research Docs — Interactions
   Academic White + Blue
   ============================ */

// ============ PARTICLE SYSTEM (light blue) ============
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.mouse = { x: -1000, y: -1000 };
        this.resize();
        this.init();
        this.bindEvents();
        this.animate();
    }

    resize() {
        this.w = this.canvas.width = window.innerWidth;
        this.h = this.canvas.height = window.innerHeight;
    }

    init() {
        const count = Math.min(Math.floor((this.w * this.h) / 18000), 60);
        this.particles = [];
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x: Math.random() * this.w,
                y: Math.random() * this.h,
                vx: (Math.random() - 0.5) * 0.4,
                vy: (Math.random() - 0.5) * 0.4,
                r: Math.random() * 2 + 0.8,
                alpha: Math.random() * 0.12 + 0.04,
            });
        }
    }

    bindEvents() {
        window.addEventListener('resize', () => { this.resize(); this.init(); });
        window.addEventListener('mousemove', (e) => { this.mouse.x = e.clientX; this.mouse.y = e.clientY; });
    }

    animate() {
        this.ctx.clearRect(0, 0, this.w, this.h);

        for (const p of this.particles) {
            p.x += p.vx;
            p.y += p.vy;
            if (p.x < 0 || p.x > this.w) p.vx *= -1;
            if (p.y < 0 || p.y > this.h) p.vy *= -1;

            const dx = p.x - this.mouse.x;
            const dy = p.y - this.mouse.y;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist < 120) {
                const force = (120 - dist) / 120;
                p.vx += (dx / dist) * force * 0.2;
                p.vy += (dy / dist) * force * 0.2;
            }
            p.vx *= 0.99;
            p.vy *= 0.99;

            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(59, 130, 246, ${p.alpha})`;
            this.ctx.fill();
        }

        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const a = this.particles[i], b = this.particles[j];
                const dx = a.x - b.x, dy = a.y - b.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    const alpha = (1 - dist / 100) * 0.06;
                    this.ctx.beginPath();
                    this.ctx.moveTo(a.x, a.y);
                    this.ctx.lineTo(b.x, b.y);
                    this.ctx.strokeStyle = `rgba(59, 130, 246, ${alpha})`;
                    this.ctx.lineWidth = 0.5;
                    this.ctx.stroke();
                }
            }
        }
        requestAnimationFrame(() => this.animate());
    }
}

// ============ SCROLL ANIMATIONS ============
class ScrollAnimator {
    constructor() {
        this.elements = document.querySelectorAll('.animate-in');
        this.navbar = document.getElementById('navbar');
        this.navLinks = document.querySelectorAll('.nav-link');
        this.sections = document.querySelectorAll('.section');
        this.init();
    }

    init() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) entry.target.classList.add('visible');
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        this.elements.forEach((el) => observer.observe(el));

        window.addEventListener('scroll', () => {
            this.navbar.classList.toggle('scrolled', window.scrollY > 50);
            this.updateActiveNav();
        });

        this.navLinks.forEach((link) => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    }

    updateActiveNav() {
        let current = '';
        this.sections.forEach((section) => {
            if (section.getBoundingClientRect().top <= 150) current = section.id;
        });
        this.navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
        });
    }
}

// ============ ARCHITECTURE NODE POPUPS (click to open) ============
class ArchPopups {
    constructor() {
        this.nodes = document.querySelectorAll('.arch-node[data-popup-title]');
        this.activePopup = null;
        this.init();
    }

    init() {
        this.nodes.forEach((node) => {
            node.addEventListener('click', (e) => {
                e.stopPropagation();
                this.togglePopup(node);
            });
        });

        document.addEventListener('click', () => this.closeAll());
    }

    togglePopup(node) {
        // Close existing
        if (this.activePopup && this.activePopup.parentElement === node) {
            this.closeAll();
            return;
        }
        this.closeAll();

        const title = node.getAttribute('data-popup-title');
        const body = node.getAttribute('data-popup-body').split('&#10;');

        const popup = document.createElement('div');
        popup.className = 'node-popup';
        popup.innerHTML = `
            <button class="popup-close" onclick="event.stopPropagation()">✕</button>
            <h4>${title}</h4>
            ${body.map(line => `<p>${line}</p>`).join('')}
        `;

        node.appendChild(popup);
        node.classList.add('selected');

        // Close button
        popup.querySelector('.popup-close').addEventListener('click', () => this.closeAll());

        // Animate in
        requestAnimationFrame(() => {
            requestAnimationFrame(() => popup.classList.add('show'));
        });

        this.activePopup = popup;
    }

    closeAll() {
        document.querySelectorAll('.node-popup').forEach(p => p.remove());
        document.querySelectorAll('.arch-node.selected').forEach(n => n.classList.remove('selected'));
        this.activePopup = null;
    }
}

// ============ INTERACTIVE SEARCH DEMO ============
class SearchDemo {
    constructor() {
        this.input = document.getElementById('demo-input');
        this.btn = document.getElementById('demo-btn');
        this.stepsContainer = document.getElementById('demo-steps');
        this.isRunning = false;

        this.synonyms = {
            'ai': ['ai', 'tri tue nhan tao', 'artificial intelligence'],
            'cntt': ['cntt', 'cong nghe thong tin', 'it', 'information technology'],
            'y hoc': ['y hoc', 'y te', 'y khoa', 'medicine'],
            'ml': ['ml', 'machine learning', 'hoc may'],
        };

        this.init();
    }

    init() {
        if (!this.btn) return;
        this.btn.addEventListener('click', () => this.run());
        this.input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') this.run();
        });
    }

    normalize(text) {
        return text.toLowerCase()
            .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
            .replace(/đ/g, 'd').replace(/Đ/g, 'D')
            .replace(/\s+/g, ' ').trim();
    }

    findSynonyms(normalized) {
        for (const [key, values] of Object.entries(this.synonyms)) {
            if (values.some(v => normalized.includes(v))) {
                return { key, values };
            }
        }
        return null;
    }

    async run() {
        const rawQuery = this.input.value.trim();
        if (!rawQuery || this.isRunning) return;

        this.isRunning = true;
        this.btn.textContent = '⏳';
        this.stepsContainer.innerHTML = '';

        const normalized = this.normalize(rawQuery);
        const syn = this.findSynonyms(normalized);

        const steps = [
            { icon: '📥', text: `Nhận query: <code>"${rawQuery}"</code>`, delay: 300 },
            { icon: '🔧', text: `Normalize: <code>"${normalized}"</code> (bỏ dấu, lowercase)`, delay: 500 },
        ];

        if (syn) {
            steps.push({
                icon: '🔄',
                text: `Synonym mở rộng: <code>${syn.key}</code> → <code>${syn.values.join(', ')}</code>`,
                delay: 600,
            });
        }

        const cacheKey = `search_cache:q:${normalized.replace(/\s/g, '+')}`;
        const cacheHit = Math.random() > 0.6;

        steps.push({
            icon: '⚡',
            text: `Redis cache check: <code>${cacheKey}</code>`,
            delay: 400,
        });

        if (cacheHit) {
            steps.push({
                icon: '✅',
                text: `Cache <strong style="color:#10b981">HIT</strong> — Trả về kết quả ngay`,
                delay: 300,
                time: '~2ms',
            });
        } else {
            steps.push({
                icon: '❌',
                text: `Cache <strong style="color:#f43f5e">MISS</strong> — Truy vấn PostgreSQL`,
                delay: 400,
            });
            steps.push({
                icon: '🗄️',
                text: `FTS: <code>search_vector @@ to_tsquery('${normalized.split(' ').join(" & ")}')</code>`,
                delay: 600,
            });
            steps.push({
                icon: '📊',
                text: `Ranking: <code>ts_rank × 2.0 + similarity</code> → sắp xếp giảm dần`,
                delay: 400,
            });
            steps.push({
                icon: '💾',
                text: `Lưu cache Redis: <code>SETEX ${cacheKey} 300</code>`,
                delay: 300,
            });
            steps.push({
                icon: '✨',
                text: `Trả về JSON response cho client`,
                delay: 200,
                time: '~50ms',
            });
        }

        for (let i = 0; i < steps.length; i++) {
            await this.delay(steps[i].delay);
            this.addStep(steps[i], i === steps.length - 1);
        }

        this.btn.textContent = 'Tìm kiếm';
        this.isRunning = false;
    }

    addStep(step, isFinal) {
        const div = document.createElement('div');
        div.className = 'demo-step';
        div.innerHTML = `
            <div class="demo-step-icon done">${step.icon}</div>
            <span>${step.text}</span>
            ${step.time ? `<span class="demo-time">${step.time}</span>` : ''}
        `;
        this.stepsContainer.appendChild(div);
        requestAnimationFrame(() => {
            requestAnimationFrame(() => div.classList.add('show'));
        });
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// ============ COLLAPSIBLE API GROUPS ============
class APIGroups {
    constructor() {
        this.groups = document.querySelectorAll('.api-group');
        this.init();
    }

    init() {
        this.groups.forEach((group) => {
            const header = group.querySelector('.api-group-header');
            header.addEventListener('click', () => {
                group.classList.toggle('collapsed');
            });
        });
    }
}

// ============ EXPANDABLE TIMELINE STEPS ============
class TimelineExpander {
    constructor() {
        this.steps = document.querySelectorAll('.timeline-step');
        this.init();
    }

    init() {
        this.steps.forEach((step) => {
            step.addEventListener('click', () => {
                // Toggle this step
                const wasExpanded = step.classList.contains('expanded');
                // Collapse all
                this.steps.forEach(s => s.classList.remove('expanded'));
                // If it wasn't expanded, expand it
                if (!wasExpanded) {
                    step.classList.add('expanded');
                }
            });
        });
    }
}

// ============ SEARCH VECTOR ROW CLICK ============
class SearchVectorHighlight {
    constructor() {
        const row = document.getElementById('col-search-vector');
        if (row) {
            row.addEventListener('click', () => {
                const detail = document.getElementById('tsvector-detail');
                if (detail) {
                    detail.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    detail.style.transition = 'box-shadow 0.4s, border-color 0.4s';
                    detail.style.boxShadow = '0 0 0 3px rgba(59, 130, 246, 0.3)';
                    detail.style.borderColor = '#3b82f6';
                    setTimeout(() => {
                        detail.style.boxShadow = '';
                        detail.style.borderColor = '';
                    }, 2000);
                }
            });
        }
    }
}

// ============ STAGGER ANIMATIONS ============
class StaggerAnimation {
    constructor() {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const items = entry.target.querySelectorAll('.container-item');
                    items.forEach((item, i) => {
                        item.style.opacity = '0';
                        item.style.transform = 'translateX(-16px)';
                        setTimeout(() => {
                            item.style.transition = 'all 0.35s ease';
                            item.style.opacity = '1';
                            item.style.transform = 'translateX(0)';
                        }, i * 80);
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        document.querySelectorAll('.container-stack').forEach(c => observer.observe(c));
    }
}

// ============ SEARCH FLOW STEP OBSERVER ============
class SearchFlowAnimator {
    constructor() {
        const flow = document.querySelector('.search-flow');
        if (!flow) return;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const steps = entry.target.querySelectorAll('.flow-step');
                    steps.forEach((step, i) => {
                        step.style.animationDelay = `${i * 0.18}s`;
                    });
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.15 });

        observer.observe(flow);
    }
}

// ============ INIT ============
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particles');
    if (canvas) new ParticleSystem(canvas);

    new ScrollAnimator();
    new ArchPopups();
    new SearchDemo();
    new APIGroups();
    new TimelineExpander();
    new SearchVectorHighlight();
    new StaggerAnimation();
    new SearchFlowAnimator();
});
