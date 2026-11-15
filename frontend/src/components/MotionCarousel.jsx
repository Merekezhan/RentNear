
import { motion, useReducedMotion } from "motion/react";
import { Link } from "react-router-dom";
import "./MotionCarousel.css";

export default function MotionCarousel({ items = [] }) {
  const reduceMotion = useReducedMotion();

  if (!items.length) return null;

  const shouldScroll = items.length >= 3;
  const cards = shouldScroll ? [...items, ...items] : items;

  return (
    <motion.section
      className="motion-showcase"
      initial={reduceMotion ? false : { opacity: 0, y: 45 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.8, ease: "easeOut" }}
    >
      <div className="motion-showcase-header">
        <div>
          <span className="motion-eyebrow">
            ✦ THE RENTNEAR COLLECTION
          </span>
          <h2>
            Discover something
            <em> extraordinary.</em>
          </h2>
          <p>
            From creative gear to everyday essentials.
            Find it nearby, rent it easily.
          </p>
        </div>

        <span className="motion-handwriting">
          made for sharing ↘
        </span>
      </div>

      <div className="motion-carousel-window">
        <div
          className={
            shouldScroll && !reduceMotion
              ? "motion-carousel-track is-moving"
              : "motion-carousel-track"
          }
        >
          {cards.map((item, index) => (
            <motion.div
              className="motion-tile"
              key={`${item.id}-${index}`}
              whileHover={
                reduceMotion
                  ? undefined
                  : {
                      y: -22,
                      scale: 1.06,
                      rotate: 0,
                      zIndex: 5
                    }
              }
              transition={{
                type: "spring",
                stiffness: 220,
                damping: 18
              }}
            >
              <Link
                to={`/items/${item.id}`}
                className="motion-product"
                tabIndex={index >= items.length ? -1 : 0}
                aria-hidden={index >= items.length ? true : undefined}
              >
                <div className="motion-product-image">
                  {item.images?.[0]?.image ? (
                    <img
                      src={item.images[0].image}
                      alt={item.title}
                      loading="lazy"
                    />
                  ) : (
                    <span className="motion-no-image">
                      ✦ RentNear
                    </span>
                  )}

                  <span className="motion-category">
                    {item.category}
                  </span>
                </div>

                <div className="motion-product-info">
                  <h3>{item.title}</h3>
                  <span className="motion-price">
                    {item.price_per_day} ₸ / day
                  </span>
                  <p>⌖ {item.location}</p>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="motion-showcase-bottom">
        <span>✳ GOOD THINGS ARE CLOSER THAN YOU THINK</span>
        <span>EXPLORE THE COLLECTION ✦</span>
      </div>
    </motion.section>
  );
}
