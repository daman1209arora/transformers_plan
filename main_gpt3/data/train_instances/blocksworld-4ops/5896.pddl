

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 )
(:init
(arm-empty)
(on b1 b5)
(on-table b2)
(on b3 b2)
(on b4 b3)
(on b5 b4)
(clear b1)
)
(:goal
(and
(on b2 b3)
(on b5 b4))
)
)


